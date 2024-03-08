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

import html


def _escape(response):
    response = html.escape(response)
    response = response.replace("(", "\\(")
    response = response.replace(")", "\\)")
    return response


def escape(response):
    if isinstance(response, str):
        return _escape(response)
    elif isinstance(response, list):
        original = list()
        for v in response:
            original.append(escape(v))
        return original
    elif isinstance(response, dict):
        original = dict()
        for k, v in response.items():
            original[_escape(k)] = escape(v)
        return original
    else:
        return response


def _unescape(response):
    response = response.replace("\\)", ")")
    response = response.replace("\\(", "(")
    response = html.unescape(response)
    return response


def unescape(response):
    if isinstance(response, str):
        return _unescape(response)
    elif isinstance(response, list):
        original = list()
        for v in response:
            original.append(unescape(v))
        return original
    elif isinstance(response, dict):
        original = dict()
        for k, v in response.items():
            original[_unescape(k)] = unescape(v)
        return original
    else:
        return response
