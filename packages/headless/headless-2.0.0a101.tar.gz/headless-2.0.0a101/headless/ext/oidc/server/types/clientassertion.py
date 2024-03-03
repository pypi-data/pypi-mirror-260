# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
import pydantic


class BaseClientAssertion(pydantic.BaseModel):
    pass


class ClientAssertion(pydantic.BaseModel):

    @classmethod
    def depends(cls):
        return fastapi.Depends(cls.parse_form)

    @classmethod
    def parse_form(
        cls,
        client_assertion_type: str | None = fastapi.Form(
            default=None,
            title="Client assertion type",
            description=(
                "The format of the assertion as defined by the authorization server. "
                "The value will be an absolute URI."
            )
        ),
        client_assertion: str | None = fastapi.Form(
            default=None,
            title="Client assertion",
            description=(
                "The assertion being used to authenticate the client. "
                "Specific serialization of the assertion is defined by the profile "
                "documents of the given `client_assertion_type`."
            )
        )
    ):
        if not any([client_assertion, client_assertion_type]):
            return None
        return cls.parse_obj({
            'assertion_type': client_assertion_type,
            'assertion': client_assertion
        })