# Copyright 2023 Fujitsu Research, Fujitsu Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import sys
import time
from importlib.metadata import entry_points
from pathlib import Path
from typing import Tuple

import pkg_resources
import requests
import toml
from jsonrpcclient.requests import request_random
from jsonrpcclient.responses import Ok, parse
from sapientml.params import Dataset, Task
from sapientml.util.json_util import JSONDecoder, JSONEncoder
from sapientml.util.logging import setup_logger
from sapientml_core import SapientMLGenerator
from sapientml_core.params import DatasetSummary

from .anonymize import Anonymizer
from .auth import Authenticator
from .escape_util import unescape
from .params import ErrorParameters, FujitsuAutoMLConfig, Pipeline, ResultParameters, summarize_dataset

model_dir_path_default = Path(__file__).parent / "models"

logger = setup_logger()

pyproject_path = Path(__file__).parents[1] / "pyproject.toml"
if pyproject_path.exists():
    with open(pyproject_path, "r", encoding="utf-8") as f:
        pyproject = toml.load(f)
    FUJITSU_AUTOML_VERSION = str(pyproject["tool"]["poetry"]["version"])
else:
    FUJITSU_AUTOML_VERSION = pkg_resources.get_distribution("fujitsu-automl").version

FUJITSU_AUTOML_ENDPOINT = os.environ.get("FUJITSU_AUTOML_ENDPOINT", "https://sapientml.azure-api.net/v3/rpc")


class FujitsuAutoMLGenerator(SapientMLGenerator):
    def __init__(self, **kwargs):
        kwargs["client_id"] = os.environ.get("FUJITSU_AUTOML_CLIENT_ID")
        self.config = FujitsuAutoMLConfig(**kwargs)
        self.config.postinit()
        eps = entry_points(group="sapientml.code_block_generator")
        self.loaddata = eps["loaddata"].load()(**kwargs)
        self.preprocess = eps["preprocess"].load()(**kwargs)
        self.dry_run = kwargs["dry_run"] if "dry_run" in kwargs else False

    @staticmethod
    def _call_api(auth: Authenticator, url: str, anonymizer: Anonymizer, request_data: str):
        logger.info("Calling WebAPIs for generating pipelines...")
        token = auth.acquire_token()
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(
                url,
                data=request_data,  # type: ignore
                timeout=100,
                headers=headers,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            message = f"JSONRPC request failed(method: generate_code): {e}\nrequest_data = {request_data}"
            raise RuntimeError(message) from e

        parsed = parse(response.json())

        if isinstance(parsed, Ok):
            uuid = parsed.result["uuid"]
            logger.info(f"Experiment Id: {uuid}")
        else:
            message = f"JSONRPC returns error(method: generate_code): {parsed.message}"  # type: ignore
            raise RuntimeError(message)

        for _ in range(100):
            time.sleep(1)
            _params = {
                "version": FUJITSU_AUTOML_VERSION,
                "uuid": uuid,
            }
            try:
                response = requests.post(
                    url,
                    json=request_random("get_result", params=_params),
                    timeout=100,
                    headers=headers,
                )
                response.raise_for_status()

            except requests.exceptions.RequestException as e:
                message = f"JSONRPC request failed(method: get_result): {e}"
                raise RuntimeError(message) from e

            parsed = parse(response.json())

            if isinstance(parsed, Ok):
                status = parsed.result["status"]
                if status == "Succeeded":
                    break
                elif status == "Failed":
                    error_json = parsed.result["error"]
                    error_json = unescape(error_json)
                    error = ErrorParameters.model_validate(error_json)
                    error = anonymizer.deanonymize(error)
                    message = f"Error occurred in version {error.version}: {error.message}"  # type: ignore
                    raise RuntimeError(message)
            else:
                message = f"JSONRPC returns error(method: get_result): {parsed.message}"  # type: ignore
                raise RuntimeError(message)

        if parsed.result["status"] != "Succeeded":
            raise RuntimeError("Could not get a successful response until 100 retries.")

        return parsed

    def generate_code(self, dataset: Dataset, task: Task) -> Tuple[Dataset, list[Pipeline]]:
        df = dataset.training_dataframe
        # Generate the meta-features
        logger.info("Generating meta features...")
        dataset_summary = summarize_dataset(df, task)  # type: ignore
        if dataset_summary.has_inf_value_targets:
            raise ValueError("Stopped generation because target columns have infinity value.")

        # discard columns with analysis
        # NOTE: The following code modify task.ignore_columns because ignore_columns is the same instance as task.ignore_columns.
        # 1. columns marked as STR_OTHER
        # if ps_macros.STR_OTHER in dataset_summary.meta_features_pp:
        #     undetermined_column_names = dataset_summary.meta_features_pp[ps_macros.STR_OTHER]
        #     if isinstance(undetermined_column_names, list):
        #         task.ignore_columns += undetermined_column_names
        #     del dataset_summary.meta_features_pp[ps_macros.STR_OTHER]
        # # 2. columns with all null values
        # if ps_macros.ALL_MISSING_PRESENCE in dataset_summary.meta_features_pp:
        #     column_names_with_all_missing_values = dataset_summary.meta_features_pp[ps_macros.ALL_MISSING_PRESENCE]
        #     if isinstance(column_names_with_all_missing_values, list):
        #         task.ignore_columns += column_names_with_all_missing_values
        #     del dataset_summary.meta_features_pp[ps_macros.ALL_MISSING_PRESENCE]

        url = FUJITSU_AUTOML_ENDPOINT
        auth = Authenticator()
        config = self.config
        config.client_id = auth.get_client_id()
        org_columns = dataset.training_dataframe.columns.tolist()

        ids = set(org_columns) | set(dataset_summary.columns)
        if config.id_columns_for_prediction is not None:
            ids |= set(config.id_columns_for_prediction)
        if config.use_word_list:
            ids |= set(config.use_word_list.keys() if isinstance(config.use_word_list, dict) else config.use_word_list)
        if dataset_summary.cols_almost_missing_string:
            ids |= set(dataset_summary.cols_almost_missing_string)
        if dataset_summary.cols_almost_missing_numeric:
            ids |= set(dataset_summary.cols_almost_missing_numeric)

        anonymizer = Anonymizer(ids)
        task = anonymizer.anonymize(task)  # type: ignore
        dataset_summary = anonymizer.anonymize(dataset_summary)
        config = anonymizer.anonymize(config)

        _params = {
            "version": FUJITSU_AUTOML_VERSION,
            "task": task.model_dump(),
            "dataset_summary": dataset_summary.model_dump(),
            "config": config.model_dump(),
        }

        if self.dry_run:
            with open("request_parameters.json", "w") as f:
                f.write(json.dumps(_params))

            logger.info("request parameters is dumped in ./request_parameters.json")
            sys.exit(0)

        request_data = json.dumps(request_random("generate_code", params=_params), cls=JSONEncoder)

        if self.config.debug:
            from fujitsu_automl_core import generate

            params = json.loads(request_data, cls=JSONDecoder)
            params = params["params"]
            task = Task(**params["task"])
            dataset_summary = DatasetSummary(**params["dataset_summary"])
            config = FujitsuAutoMLConfig(**params["config"])
            pipelines, labels = generate(task, config, dataset_summary)
            result = ResultParameters(pipelines=pipelines, labels=labels)
            result_json = result.model_dump()
        else:
            parsed = self._call_api(auth, url, anonymizer, request_data)
            result_json = parsed.result["result"]

        try:
            result_json = unescape(result_json)
            result = ResultParameters.model_validate(result_json)
            result = anonymizer.deanonymize(result)
        except Exception as e:
            message = f"Convert Error(from dict to dataclass): {e}"
            raise RuntimeError(message)

        return dataset, result.pipelines  # type: ignore
