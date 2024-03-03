# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Literal

from headless.types import ICredential
from headless.types import IRequest

from .provider import Server


class ClientSecretCredential(ICredential):
    __module__: str = 'headless.ext.oidc'

    def __init__(
        self,
        server: Server[Any],
        client_id: str,
        client_secret: str,
        mode: Literal['client_secret_post', 'client_secret_basic', 'client_secret_jwt'] | None = None,
        algorithm: str | None = None
    ):
        self.algorithm = algorithm
        self.client_id = client_id
        self.client_secret = client_secret
        self.mode = mode
        self.server = server

    async def add_to_request(self, request: IRequest[Any]) -> None:
        if not self.server.is_protected(str(request.url)):
            return
        if self.mode == 'client_secret_basic':
            raise NotImplementedError

    async def preprocess_request( # type: ignore
        self,
        url: str,
        json: dict[str, str] | None,
        data: dict[str, str] | None,
        **kwargs: dict[str, Any]
    ) -> dict[str, Any] | None:
        if (data or json) and not bool(json) ^ bool(data):
            raise TypeError("Provide either 'data' or 'json'.")
        if self.server.is_protected(url):
            params: dict[str, Any] = data or json or {}
            if self.mode == 'client_secret_post':
                params.update({
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                })
        return {**kwargs, 'url': url, 'json': json, 'data': data}

    def must_authenticate(self, endpoint: str) -> bool:
        return self.server.is_protected(endpoint)