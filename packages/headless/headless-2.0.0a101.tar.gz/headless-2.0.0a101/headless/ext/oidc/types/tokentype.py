# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`TokenType`."""
import enum


class TokenType(str, enum.Enum):
    access_token = 'urn:ietf:params:oauth:token-type:access_token'
    refresh_token = 'urn:ietf:params:oauth:token-type:refresh_token'
    id_token = 'urn:ietf:params:oauth:token-type:id_token'
    saml1 = 'urn:ietf:params:oauth:token-type:saml1'
    saml2 = 'urn:ietf:params:oauth:token-type:saml2'
    jwt = 'urn:ietf:params:oauth:token-type:jwt'