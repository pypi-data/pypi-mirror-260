# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import fastapi
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials
from headless.ext.oidc.types import FatalError
from headless.ext.oidc.types import InvalidRequest

from ..nullclient import NullClient
from ..types import ClientAssertion
from ..types import IClient
from ..types import IServerStorage
from ..utils import set_signature_defaults


async def get(
    storage: IServerStorage = NotImplemented,
    basic_auth: HTTPBasicCredentials | None = fastapi.Depends(HTTPBasic(auto_error=False)),
    client_id: str | None = fastapi.Form(
        default=None,
        title="Client ID",
        description=(
            "Identifies the client application that is issueing the request. "
            "This parameter is **required** if the client is public or "
            "uses HTTP POST parameters to authenticate itself, otherwise "
            "it **must** be omitted.\n\n"
            "The `client_id` is unnecessary when using client assertion "
            "authentication because the client is identified by the subject "
            "of the assertion.  If present, the value of the `client_id` "
            "parameter **must** identify the same client as is identified "
            "by the client assertion."
        )
    ),
    client_secret: str | None = fastapi.Form(
        default=None,
        title="Client secret",
        description=(
            "The shared secret of the client, if HTTP POST "
            "parameters are used to authenticate."
        )
    ),
    client_assertion: ClientAssertion | None = ClientAssertion.depends()
) -> IClient:
    assert storage != NotImplemented

    # The client did not provide any identification or authentication.
    if not any([basic_auth, client_assertion, client_secret]):
        client = NullClient()
        if client_id:
            # Points to a public client. Lookup the client and determine
            # if it is public, and return the client.
            raise NotImplementedError
        return client

    # If an assertion is invalid for any reason or if more than one
    # client authentication mechanism is used, the authorization
    # server constructs an error response as defined in RFC 6749.
    # The value of the "error" parameter MUST be the "invalid_client"
    # error code.  The authorization server MAY include additional
    # information regarding the reasons the client assertion was
    # considered invalid using the "error_description" or "error_uri"
    # parameters.
    if len(list(filter(bool, [basic_auth, client_assertion, client_secret]))) > 1:
        raise FatalError(
            error='invalid_client',
            error_description='A single method for client authentication must be used'
        )
    
    # If the client_secret parameter is used, then the client_id parameter
    # is mandatory.
    if not client_id and client_secret:
        raise InvalidRequest("The client_id parameter is required.")

    raise NotImplementedError


def CurrentClient(
    storage_class: Any
) -> Any:
    return fastapi.Depends(set_signature_defaults(get, {
        'storage': fastapi.Depends(storage_class)
    }))