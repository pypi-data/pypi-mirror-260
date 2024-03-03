# Copyright (C) 2023 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import decimal

import pydantic


class OrderItem(pydantic.BaseModel):
    id: int
    item_identifier: str | None = None
    name: str
    parcel_tracking_url: str | None = None
    sku: str
    taxation: str
    total_charged: decimal.Decimal