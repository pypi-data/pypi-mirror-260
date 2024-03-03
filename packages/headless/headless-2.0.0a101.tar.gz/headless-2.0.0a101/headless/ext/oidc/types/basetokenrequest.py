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
from typing import TypeAlias
from typing import Union

import pydantic

from headless.types import IClient
from headless.types import ICredential
from headless.types import IRequest
from headless.types import IResponse
from .tokentype import TokenType


__all__: list[str] = [
    'AccessTokenRequest',
    'AuthorizationCodeTokenRequest',
    'BaseTokenRequest',
    'JWTBearerRequest',
    'RefreshTokenRequest',
]


class BaseTokenRequest(pydantic.BaseModel):
    resource: str | None = pydantic.Field(
        default=None,
        description=(
            "Specifies the intended resource to use the issued access token and "
            "(optionally) ID token with."
        )
    )


class AuthorizationCodeTokenRequest(BaseTokenRequest):
    grant_type: Literal['authorization_code'] = pydantic.Field(
        default=...,
        description="This value **must** be `authorization_code`."
    )

    code: str = pydantic.Field(
        default=...,
        description="The authorization code received from the authorization server"
    )

    redirect_uri: str | None = pydantic.Field(
        default=None,
        description=(
            "This parameter is **required** if the `redirect_uri` parameter was "
            "included in the authorization request and their values **must** be identical."
        )
    )

    client_id: str | None = pydantic.Field(
        default=None,
        description=(
            "This parameter is **required** if the client is not authenticating with "
            "the authorization server."
        )
    )


class ClientCredentialsRequest(BaseTokenRequest):
    grant_type: Literal['client_credentials'] = pydantic.Field(
        default=...,
        description="This value **must** be `client_credentials`."
    )

    scope: str | None = pydantic.Field(
        default=None,
        description="The space-delimited scope of the access request."
    )


class JWTBearerRequest(BaseTokenRequest):
    grant_type: Literal['urn:ietf:params:oauth:grant-type:jwt-bearer'] = pydantic.Field(
        default=...,
        description="This value **must** be `urn:ietf:params:oauth:grant-type:jwt-bearer`."
    )

    assertion: str = pydantic.Field(
        default=...,
        description=(
            "A string containing a single JSON Web Token (JWT)."
        )
    )

    scope: str | None = pydantic.Field(
        default=None,
        description="The space-delimited scope of the access request."
    )


class RefreshTokenRequest(BaseTokenRequest):
    grant_type: Literal['refresh_token'] = pydantic.Field(
        default=...,
        description="This value **must** be `refresh_token`."
    )

    refresh_token: str = pydantic.Field(
        default=...,
        description="The refresh token that was issued to the client."
    )

    scope: str | None = pydantic.Field(
        default=None,
        description=(
            "The space-delimited scope of the access request. The requested "
            "scope **must not** include any scope not originally granted by "
            "the resource owner, and if omitted is treated as equal to the "
            "scope originally granted by the resource owner."
        )
    )


class TokenExchangeRequest(BaseTokenRequest):
    audience: str | None = pydantic.Field(
        default=None,
        description=(
            "The logical name of the target service where the client "
            "intends to use the requested security token. This serves "
            "a purpose similar to the `resource` parameter but with the "
            "client providing a logical name for the target service"
        )
    )

    grant_type: str = pydantic.Field(
        default=...,
        description=(
            "The value `urn:ietf:params:oauth:grant-type:token-exchange` "
            "indicates that a token exchange is being performed."
        )
    )

    requested_token_type: TokenType | None = pydantic.Field(
        default=None,
        title="Requested token type",
        description=(
            "An identifier for the type of the requested security token. If "
            "the requested type is unspecified, the issued token type is at "
            "the discretion of the authorization server and may be dictated "
            "by knowledge of the requirements of the service or resource "
            "indicated by the resource or audience parameter."
        )
    )

    subject_token: str = pydantic.Field(
        default=...,
        title="Subject token",
        description=(
            "A security token that represents the identity of the party on "
            "behalf of whom the request is being made. Typically, the "
            "subject of this token will be the subject of the security "
            "token issued in response to the request."
        )
    )

    subject_token_type: TokenType = pydantic.Field(
        default=...,
        title="Subject token type",
        description=(
            "An identifier that indicates the type of the security "
            "token in the `subject_token` parameter."
        )
    )

    actor_token: str | None = pydantic.Field(
        default=None,
        title="Actor token",
        description=(
            "A security token that represents the identity of the acting party."
             " Typically, this will be the party that is authorized to use the "
             " requested security token and act on behalf of the subject."
        )
    )

    actor_token_type: TokenType = pydantic.Field(
        default=None,
        title="Actor token type",
        description=(
            "An identifier that indicates the type of the security token in "
            "the `actor_token` parameter. This is **required** when the "
            "`actor_token` parameter is present in the request but **must "
            "not** be included otherwise"
        )
    )


class AccessTokenRequest(pydantic.BaseModel):
    __root__: Union[
        AuthorizationCodeTokenRequest,
        ClientCredentialsRequest,
        JWTBearerRequest,
        RefreshTokenRequest,
        TokenExchangeRequest
    ]

    async def send(
        self,
        client: IClient[IRequest[Any], IResponse[Any, Any]],
        url: str,
        credential: ICredential
    ) -> IResponse[Any, Any]:
        return await client.post(
            url=url,
            data=self.__root__.dict(exclude_none=True),
            credential=credential
        )