# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from headless.ext.oidc.types import TokenResponse


class BaseTokenIssuer:
    __module__: str = 'cbra.ext.oidc.server'

    async def authenticate(self) -> None:
        pass

    async def issue(self, params: Any) -> TokenResponse:
        """Issue an access token using the given parameters."""
        await self.authenticate()