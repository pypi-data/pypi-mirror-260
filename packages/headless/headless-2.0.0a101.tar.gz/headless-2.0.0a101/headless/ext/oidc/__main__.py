# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
import uvicorn

from .server import BaseTokenIssuer
from .server import OIDCEndpointRouter
from .server.types import IServerStorage


class TokenIssuer(BaseTokenIssuer):
    pass


class ServerStorage(IServerStorage):

    def __init__(self) -> None:
        pass


app: fastapi.FastAPI = fastapi.FastAPI()
app.include_router(
    prefix='/oauth/v2',
    router=OIDCEndpointRouter(
        issuer=TokenIssuer,
        storage=ServerStorage
    )
)


if __name__ == '__main__':
    uvicorn.run('headless.ext.oidc.__main__:app', reload=True) # type: ignore