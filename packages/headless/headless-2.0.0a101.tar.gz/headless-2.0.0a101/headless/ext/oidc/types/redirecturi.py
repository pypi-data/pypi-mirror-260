# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import ipaddress
import urllib.parse
from typing import Any
from typing import Callable
from typing import Generator
from typing import TypeVar

from pydantic.validators import str_validator

from .fatalerror import InvalidRequest


T = TypeVar('T', bound='RedirectURI')


OOB_URLS: set[str] = {
    "urn:ietf:wg:oauth:2.0:oob",
    "urn:ietf:wg:oauth:2.0:oob:auto"
}


class RedirectURI(str):
    __module__: str = 'headless.ext.oidc.types'
    params: dict[str, str]

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: dict[str, Any]
    ) -> None:
        field_schema.update( # pragma: no cover
            title='Redirect URI',
            type='string',
            format='url'
        )

    @classmethod
    def __get_validators__(cls: type[T]) -> Generator[Callable[..., str | T], None, None]:
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls: type[T], v: str) -> T:
        if len(v) > 2048:
            raise InvalidRequest('The redirect_uri parameter is too long to be a valid URL.')
        if v in OOB_URLS:
            raise InvalidRequest('OOB is a security risk.')
        p = urllib.parse.urlparse(v)
        if not p.scheme or not p.netloc:
            raise InvalidRequest('The redirect_uri parameter did not specify a valid URL.')
        if p.query:
            raise InvalidRequest('Query parameters must not be used in the redirect URI.')
        if p.fragment:
            raise InvalidRequest('URL fragment must not be used in the redirect URI.')

        # Check if the value is an IP address.
        if p.hostname:
            try:
                ip = ipaddress.ip_address(p.hostname)
            except ValueError:
                # Not a valid ip address. The hostname points to a domain
                if p.scheme != 'https':
                    raise InvalidRequest('the https scheme must be used.')
            else:
                if not ip.is_loopback and p.scheme != 'https':
                    raise InvalidRequest('the https scheme must be used.')

            if p.hostname == 'localhost':
                # Clients should use loopback IP literals rather than the
                # string localhost as described in Section 8.4.2.
                # (OAuth 2.1 draft).
                raise InvalidRequest('local redirect URIs must use loopback IP literals.')

        return cls(urllib.parse.urlunparse(p))

    def redirect(self, allow_params: bool = False, **params: Any) -> str:
        """Create a redirect URI with the given params."""
        p: list[str] = list(urllib.parse.urlparse(self)) # type: ignore
        params = {k: v for k, v in params.items() if v is not None}
        if allow_params:
            params.update(urllib.parse.parse_qsl(p[4]))
        p[4] = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return urllib.parse.urlunparse(p)

    def __repr__(self) -> str: # pragma: no cover
        return f'RedirectURI({self})'