# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import itertools

from ..resource import TeamleaderResource
from .company import Company
from .contact import Contact
from .invoice import Invoice
from .invoicedparty import InvoiceParty
from .invoicelineitemsection import InvoiceLineItem
from .invoicelineitemsection import InvoiceLineItemSection
from .resourcereference import ResourceReference



class CreditNote(TeamleaderResource):
    created_at: datetime.datetime
    credit_note_number: str | None
    department: ResourceReference
    paid: bool
    id: str
    status: str
    grouped_lines: list[InvoiceLineItemSection] = []
    invoice: ResourceReference
    invoicee: InvoiceParty
    
    @property
    def invoice_date(self) -> datetime.date:
        return self.created_at.date()

    @property
    def items(self) -> list[InvoiceLineItem]:
        return list(itertools.chain(*[x.line_items for x in self.grouped_lines]))

    @property
    def number(self) -> str | None:
        return self.credit_note_number

    async def get_invoice(self) -> Invoice:
        return await self._client.retrieve(Invoice, self.invoice.id)

    async def get_invoicee(self) -> Company | Contact:
        cls = Company if self.invoicee.customer.type == 'company' else Contact
        return await self._client.retrieve(cls, self.invoicee.customer.id)

    class Meta(TeamleaderResource.Meta):
        base_endpoint: str = '/creditNotes'