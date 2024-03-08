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

from pydantic import BaseModel

EXTS = [".pkl", ".csv", ".tsv"]


class Anonymizer:
    def __init__(self, columns: set[str]):
        self.dict: dict[str, str] = dict()
        self.rev_dict: dict[str, str] = dict()
        for i, original in enumerate(columns):
            anonymized = f"anonymous_id_{i+1}"
            for ext in EXTS:
                if original.endswith(ext):
                    anonymized = f"{anonymized}{ext}"
                    break
            self.dict[original] = anonymized
            self.rev_dict[anonymized] = original

    def _anonymize_str(self, original) -> str:
        return self.dict[original] if original in self.dict else original

    def _deanonymize_str(self, anonymized: str) -> str:
        return self.rev_dict[anonymized] if anonymized in self.rev_dict else anonymized

    def _deanonymize_code(self, code: str) -> str:
        for anonymized, original in self.rev_dict.items():
            if "\\" in original:
                original = original.replace("\\", "\\\\")
            single_quote_flag = "'" in original
            double_quote_flag = '"' in original
            quote = "'"
            if single_quote_flag and double_quote_flag:
                original = original.replace("'", "\\'")
            elif single_quote_flag:
                quote = '"'
            code = code.replace(f"'{anonymized}'", f"{quote}{original}{quote}").replace(
                f'"{anonymized}"', f"{quote}{original}{quote}"
            )
        return code

    def _anonymize(self, original):
        if isinstance(original, str):
            return self._anonymize_str(original)
        elif isinstance(original, list):
            anonymized = list()
            for v in original:
                anonymized.append(self._anonymize(v))
            return anonymized
        elif isinstance(original, dict):
            anonymized = dict()
            for k, v in original.items():
                anonymized[self._anonymize_str(k)] = self._anonymize(v)
            return anonymized
        elif isinstance(original, BaseModel):
            return self.anonymize(original)
        else:
            return original

    def anonymize(self, original: BaseModel) -> BaseModel:
        anonymized = dict()
        for k, v in original.dict().items():
            anonymized[k] = self._anonymize(v)
        return original.__class__(**anonymized)

    def _deanonymize(self, anonymized):
        if isinstance(anonymized, str):
            return self._deanonymize_str(anonymized)
        elif isinstance(anonymized, list):
            original = list()
            for v in anonymized:
                original.append(self._deanonymize(v))
            return original
        elif isinstance(anonymized, dict):
            original = dict()
            for k, v in anonymized.items():
                if k in ("validation", "test", "train", "predict"):
                    original[k] = self._deanonymize_code(v)
                elif k == "code" and isinstance(v, list):
                    original[k] = [self._deanonymize_code(_v) for _v in v]
                else:
                    original[self._deanonymize_str(k)] = self._deanonymize(v)
            return original
        elif isinstance(anonymized, BaseModel):
            return self.deanonymize(anonymized)
        else:
            return anonymized

    def deanonymize(self, anonymized: BaseModel) -> BaseModel:
        original = dict()
        for k, v in anonymized.dict().items():
            original[self._deanonymize_str(k)] = self._deanonymize(v)
        return anonymized.__class__(**original)
