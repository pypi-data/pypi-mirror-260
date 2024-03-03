# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable
from typing import Coroutine

import fastapi
import pydantic
from starlette.responses import Response

from headless.ext.oidc.types import Error
from headless.ext.oidc.types import FatalError
from headless.ext.oidc.types import InvalidRequest
from headless.ext.oidc.types import BaseTokenRequest
from headless.ext.oidc.types import JWTBearerRequest
from headless.ext.oidc.types import GrantType
from headless.ext.oidc.types import TokenResponse
from .basetokenissuer import BaseTokenIssuer
from .params import CurrentClient
from .types import IClient
from .types import IServerStorage
from .types import ITokenIssuer
from .utils import set_signature_defaults


__all__: list[str] = [
    'BaseTokenIssuer',
    'OIDCEndpointRouter',
]


class OIDCEndpointRouter(fastapi.APIRouter):
    __module__: str = 'cbra.ext.oidc.OIDCEndpointRouter'
    authorization_grants: dict[GrantType, type[BaseTokenRequest]] = {
        GrantType.jwt_bearer: JWTBearerRequest
    }

    class token_endpoint_route_class(fastapi.routing.APIRoute):

        def get_route_handler(self) -> Callable[[fastapi.Request], Coroutine[Any, Any, Response]]:
            handler = super().get_route_handler()

            async def f(request: fastapi.Request) -> Response:
                errors: list[Error] = []
                try:
                    return await handler(request)
                except Error as exc:
                    return fastapi.responses.JSONResponse(
                        status_code=400,
                        content={
                            'error': exc.error,
                            'error_description': exc.error_description
                        }
                    )
                except (fastapi.exceptions.RequestValidationError, pydantic.ValidationError) as exc:
                    for error in exc.errors():
                        param = error['loc'][-1]
                        t = error.get('type')
                        match t:
                            case "value_error.missing":
                                errors.append(InvalidRequest(f'The {param} parameter is required.'))
                            case "type_error.none.not_allowed":
                                errors.append(InvalidRequest(f'The {param} parameter is required.'))
                            case "type_error.enum":
                                if param == 'grant_type':
                                    errors.append(
                                        FatalError(
                                            error='unsupported_grant_type',
                                            error_description=(
                                                "The authorization server does not support the requested "
                                                "grant type, or the grant type is not allowed for this "
                                                "client."
                                            )
                                        )
                                    )
                                else:
                                    errors.append(InvalidRequest(f"Invalid value provided for the {param} parameter."))
                            case _:
                                continue
                    if not errors:
                        raise NotImplementedError(exc)
                except Exception:
                    return fastapi.responses.JSONResponse(
                        status_code=500,
                        content={
                            'error': 'server_error',
                            'error_description': 'The authorization server encountered an unexpected condition that prevented it from fulfilling the request.'
                        }
                    )

                assert errors
                return fastapi.responses.JSONResponse(
                    status_code=400,
                    content=errors[0].dict()
                )

            return f

    def __init__(
        self,
        *,
        issuer: type[ITokenIssuer],
        storage: type[IServerStorage],
        token_handler: bool = False
    ):
        super().__init__()
        if token_handler:
            raise NotImplementedError
        else:
            self.add_api_route(
                path='/token',
                endpoint=set_signature_defaults(self.token, {
                    'client': CurrentClient(storage),
                    'issuer': fastapi.Depends(issuer)
                }),
                name='oauth2.token',
                summary="Token endpoint",
                methods=['POST'],
                route_class_override=self.token_endpoint_route_class,
                tags=['OAuth 2.x/OpenID Connect']
            )

    async def token(
        self,
        client: IClient = NotImplemented,
        issuer: ITokenIssuer = NotImplemented,
        grant_type: GrantType = fastapi.Form(
            default=...,
            title="Grant type",
            description=(
                "Specifies the authorization grant type used."
            )
        ),
        assertion: str | None = fastapi.Form(
            default=None,
            title="Assertion",
            description=(
                "The assertion being used as an authorization grant. Specific "
                "serialization of the assertion is defined by the profile documents "
                "of the specified `grant_type`."
            )
        ),
        resources: list[str] = fastapi.Form(
            default=[],
            alias='resource',
            title="Resource",
            description=(
                "A URI that indicates the target service or resource where "
                "the client intends to use the requested security token. "
                "The value of the `resource` parameter **must** be an "
                "absolute URI, as specified by Section 4.3 of RFC 3986, "
                "that **may** include a query component and **must not** "
                "include a fragment component. Multiple resource parameters "
                "may be used to indicate that the issued token is intended "
                "to be used at the multiple resources listed."
            )
        ),
        scope: str | None = fastapi.Form(
            default=None,
            title="Scope",
            description=(
                "The requested scope as described in Section 3.3 of OAuth 2.0 "
                "(RFC 6749). The requested scope **must** be equal to or less "
                "than the scope originally granted to the authorized accessor."
            )
        ),
    ) -> TokenResponse:
        """The token endpoint is used by the client to obtain an access
        token by presenting its authorization grant or refresh token.
        The token endpoint is used with every authorization grant except
        for the implicit grant type (since an access token is issued directly).

        **JSON Web Token (JWT) Authorization Grant**
        """
        assert issuer != NotImplemented
        if grant_type not in self.authorization_grants:
            FatalError(
                error='unsupported_grant_type',
                error_description=(
                    "The authorization server does not support the requested "
                    "grant type, or the grant type is not allowed for this "
                    "client."
                )
            )
        params = self.authorization_grants[grant_type].parse_obj({
            'grant_type': grant_type,
            'assertion': assertion,
            'resources': resources,
            'scope': scope,
        })
        return await issuer.issue(params)