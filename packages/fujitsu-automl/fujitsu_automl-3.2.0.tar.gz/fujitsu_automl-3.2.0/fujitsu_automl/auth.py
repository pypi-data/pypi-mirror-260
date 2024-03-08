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
from pathlib import Path

import msal
from sapientml.util.logging import setup_logger

logger = setup_logger()


class Authenticator:
    def __init__(self):
        AUTHORITY = os.environ.get("FUJITSU_AUTOML_AUTHORITY")
        CLIENT_ID = os.environ.get("FUJITSU_AUTOML_CLIENT_ID")
        CLIENT_SECRET = os.environ.get("FUJITSU_AUTOML_CLIENT_SECRET")
        CONFIDENTIAL_CLIENT_SCOPE = os.environ.get("FUJITSU_AUTOML_CONFIDENTIAL_CLIENT_SCOPE")
        PUBLIC_CLIENT_SCOPE = os.environ.get("FUJITSU_AUTOML_PUBLIC_CLIENT_SCOPE")
        self._CLIENT_ID = CLIENT_ID

        if CLIENT_SECRET is not None:
            self.app = msal.ConfidentialClientApplication(
                CLIENT_ID,
                authority=AUTHORITY,
                client_credential=CLIENT_SECRET,
            )
            self.SCOPE = [CONFIDENTIAL_CLIENT_SCOPE]
            self.cache_path = None
        else:
            self.cache = msal.SerializableTokenCache()
            self.cache_path = Path(__file__).absolute() / "cache.bin"
            if os.path.exists(self.cache_path):
                self.cache.deserialize(open(self.cache_path, "r").read())

            self.app = msal.PublicClientApplication(
                CLIENT_ID,
                authority=AUTHORITY,
                token_cache=self.cache,
            )
            self.SCOPE = [PUBLIC_CLIENT_SCOPE]

    def _acquire_token_for_client(self):
        assert isinstance(self.app, msal.ConfidentialClientApplication)

        logger.info("Authenticating app via OAuth 2.0 Client Credentials Flow")

        return self.app.acquire_token_for_client(scopes=self.SCOPE)

    def _acquire_token_for_device(self) -> dict:
        assert isinstance(self.app, msal.PublicClientApplication)

        logger.info("Authenticating app via OAuth 2.0 Device Code Flow")

        accounts = self.app.get_accounts()
        if accounts:
            logger.info(f'Using the cached token of {accounts[0]["username"]}')
            chosen = accounts[0]
            return self.app.acquire_token_silent(
                self.SCOPE,
                account=chosen,
            )  # type: ignore

        flow = self.app.initiate_device_flow(scopes=self.SCOPE)
        if "user_code" not in flow:
            raise ValueError(f"Fail to create device flow. Error: {json.dumps(flow, indent=4)}")

        logger.warn(
            f"""
**********************************************************************

{flow["message"]}

**********************************************************************
"""
        )

        result = self.app.acquire_token_by_device_flow(flow)

        if self.cache.has_state_changed and self.cache_path is not None:
            with open(self.cache_path, "w") as f:
                f.write(self.cache.serialize())

        return result

    def acquire_token(self) -> str:
        if isinstance(self.app, msal.ConfidentialClientApplication):
            result = self._acquire_token_for_client()
        else:
            result = self._acquire_token_for_device()

        if isinstance(result, dict):
            if "access_token" in result:
                return result["access_token"]

            raise RuntimeError(
                f'{result.get("error")}\n{result.get("error_description")}\n{result.get("correlation_id")}'
            )
        else:
            raise RuntimeError(f"Error in authentication: {result}")

    def get_client_id(self) -> str:
        return self._CLIENT_ID
