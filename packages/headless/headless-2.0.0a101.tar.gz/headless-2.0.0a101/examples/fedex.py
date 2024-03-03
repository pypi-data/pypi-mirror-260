# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio

from headless.ext.fedex import FedexClient


ACCOUNT_NUMBER: str = '801014461'
ACCOUNT_NUMBER: str = '734633992' # type: ignore

# 774623876998
# 774623983639
# 774624002225
# 774624063558
# 774624201750
# 774624384613
# 774624454381
# 774624652557
# 774624733863
# 774625112523

async def main():
    params = {
        #'url': 'https://apis-sandbox.fedex.com',
        'url': 'https://apis.fedex.com',
        'client_id': 'l79909e629af7d42e4be3c7c207f22ecfc',
        'client_secret': '5bec324f-b943-4dc6-9eba-43b9742a7f9e'
    }
    async with FedexClient(**params) as client:
        response = await client.put(
            url='/ship/v1/shipments/cancel',
            json={
                'accountNumber': {'value': ACCOUNT_NUMBER},
                'emailShipment': False,
                'senderCountryCode': 'NL',
                'deletionControl': 'DELETE_ALL_PACKAGES',
                'trackingNumber': '774625112523',
            }
        )
        print(await response.json())
        raise SystemExit
        response = await client.post(
            url='/ship/v1/shipments',
            json={
                "accountNumber": {"value": ACCOUNT_NUMBER},
                "labelResponseOptions": "URL_ONLY",
                'mergeLabelDocOption': 'LABELS_ONLY',
                'shipAction': 'CONFIRM',
                'processingOptionType': 'SYNCHRONOUS_ONLY',
                'requestedShipment': {
                    'shipper': {
                        'contact': {
                            'personName': "Laili Ishaqzai",
                            'emailAddress': 'finance@molano.nl',
                            'phoneNumber': '+31850601229',
                            'companyName': 'Molano B.V.'
                        },
                        'address': {
                            'streetLines': ['Hendrik Figeeweg 1/N'],
                            'city': 'Haarlem',
                            'postalCode': '2031BJ',
                            'countryCode': 'NL'
                        }
                    },
                    'recipients': [{
                        'contact': {
                            'personName': 'Cochise Ruhulessin',
                            'phoneNumber': '+31687654321',
                            'companyName': 'Immortal Industries B.V.'
                        },
                        'address': {
                            'streetLines': [
                                'Carl-Metz-Str. 4'
                            ],
                            'city': 'Ettlingen',
                            'postalCode': '76275',
                            'countryCode': 'DE'
                        }
                    }],
                    'customsClearanceDetail': {
                        'totalCustomsValue': {'amount': 0, 'currency': 'EUR'},
                        'dutiesPayment': {'paymentType': 'SENDER'},
                        'commodities': [
                            {
                                'countryOfManufacture': 'CN',
                                'unitPrice': {'amount': 1, 'currency': 'EUR'},
                                'quantity': 1,
                                'quantityUnits': 'EA',
                                'description': 'iPhone 12 Pro Max',
                                'weight': {'units': 'KG', 'value': 0.0}
                            },
                        ]
                    },
                    "shipDatestamp": "2023-12-28",
                    'shipmentSpecialServices': {
                        'specialServiceTypes': ['ELECTRONIC_TRADE_DOCUMENTS'],
                        'etdDetail': {
                            'requestedDocumentTypes': ['LABEL'],
                            #'attachedDocuments': [
                            #    {
                            #    "documentType": "PRO_FORMA_INVOICE",
                            #    "documentReference": "DocumentReference",
                            #    "description": "PRO FORMA INVOICE",
                            #    "documentId": "090927d680038c61"
                            #    }
                            #]
                        },
                    },
                    "serviceType": "FEDEX_INTERNATIONAL_PRIORITY",
                    "packagingType": "YOUR_PACKAGING",
                    "pickupType": "USE_SCHEDULED_PICKUP",
                    "blockInsightVisibility": False,
                    "shippingChargesPayment": {"paymentType": "SENDER"},
                    "labelSpecification": {
                        "imageType": "PNG",
                        "labelStockType": "PAPER_4X8"
                    },
                    "requestedPackageLineItems": [
                        {
                            "weight": {"units": "KG", "value": 0.1},
                            "packageSpecialServices": {
                                "specialServiceTypes": ["BATTERY"],
                                #'dangerousGoodsDetail': {
                                #    'accessibility': "ACCESSIBLE",
                                #    'options': ['BATTERY']
                                #},
                                'batteryDetails': [{
                                    'batteryPackingType': 'CONTAINED_IN_EQUIPMENT',
                                    "batteryRegulatoryType": "IATA_SECTION_II",
                                    'batteryMaterialType': 'LITHIUM_ION',
                                }]
                            },
                        }
                    ]
                },
            }
        )
        import json
        if response.status_code >= 400:
            print(response.content)
            raise SystemExit
        response.raise_for_status()
        dto = await response.json()
        assert len(dto['output']['transactionShipments']) == 1
        assert len(dto['output']['transactionShipments'][0]['pieceResponses']) == 1
        doc = dto['output']['transactionShipments'][0]['pieceResponses'][0]['packageDocuments'][0]
        assert doc['contentType'] == 'LABEL'
        print(dto['output']['transactionShipments'][0]['completedShipmentDetail']['masterTrackingId']['trackingNumber'])
        
        #print(json.dumps(dto, indent=2))

        import io
        from PIL import Image
        buf = io.BytesIO()
        response = await client.get(url=doc['url'])
        response.raise_for_status()
        im = Image.open(io.BytesIO(response.content))
        im.convert('RGB')
        im.save(buf, format='pdf')

        buf.seek(0)
        with open('test.pdf', 'wb') as f:
            f.write(buf.read())

        
if __name__ == '__main__':
    asyncio.run(main())