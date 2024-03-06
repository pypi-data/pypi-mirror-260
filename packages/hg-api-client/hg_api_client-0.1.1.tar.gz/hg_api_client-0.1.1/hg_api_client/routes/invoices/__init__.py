#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from datetime import datetime, timedelta

from hutki_grosh_api_client.utils import BaseRoute, RequestTypes


class ClientInvoiceRoute(BaseRoute):
    prefix = '/v1/invoicing/invoice'

    async def get(
            self,
            token: str,
            search_string: str,
    ):
        return await self.request(
            type_=RequestTypes.GET,
            parameters={
                'searchString': search_string,
            },
            response_key='records',
            token=token,
        )

    async def create(
            self,
            token: str,
            invoice_name: int,
            service_provider_id: int,
            service_provider_name: str,
            service_id: int,
            service_name: str,
            address_country: str,
            address_line: str,
            address_city: str,
            full_address: str,
            locality_code: str,
            items: list,
            store_name: str,
            store_locality_name: str,
            store_city: str,
            store_locality_city: str,
            terms_of_days: int,
    ):
        due_utc = str(datetime.utcnow() + timedelta(terms_of_days))
        return await self.request(
            type_=RequestTypes.POST,
            parameters={
                'number': invoice_name,
                'currency': '933',
                'merchantInfo': {
                    'serviceProviderId': service_provider_id,
                    'serviceProviderName': service_provider_name,
                    'serviceId': service_id,
                    'serviceName': service_name,
                    'retailOutlet': {
                        'code': 1,
                        'address': {
                            'country': address_country,
                            'line1': address_line,
                            'city': address_city,
                            'fullAddress': full_address
                        },
                        'businessCard': None,
                        'retailOutletMerchantInfo': {
                            'storeName': store_name,
                            'storeLocalityName': store_locality_name,
                            'localityCode': locality_code,
                            'storeCity': store_city,
                            'storeLocalityCity': store_locality_city,
                            'trerminalLabel': None,
                        },
                        'eripMcc': None,
                        'mcc': {
                            'code': '8999',
                            'name': None,
                        },
                        'cashBoxes': None,
                        'descr': None,
                        'notifyParams': {
                            'emails': [],
                            'smses': [],
                            'urls': [],
                            'users': [],
                            'oneSignalUsers': None,
                            'cashBoxNotifyUrl': None,
                        },
                        'state': 1,
                    },
                    'cashBox': None,
                },
                'items': [
                    {
                        'code': item['name'],
                        'name': item['name'],
                        'description': item['description'],
                        'quantity': item['quantity'],
                        'unitPrice': {
                            'value': item['price'],
                        },
                        'measure': 'string',
                        'discount': {
                            'percent': item['discount_percent'],
                            'amount': item['discount_amount'],
                        }
                    } for item in items
                ],
                'paymentRules': {
                    'isTariff': False,
                    'isTariffExpire': False,
                    'requestAmount': False,
                    'requestAddress': False,
                    'requestPersonName': False,
                    'requestPhone': False,
                    'requestEMail': False,
                    'requestLoyalityNumber': False,
                    'requestPurpose': False,
                    'requestReferenceLoyalityNumber': False,
                    'canMakeStorno': False,
                    'partialPymentay': False,
                },
                'paymentDueTerms': {
                    'dueUTC': due_utc,
                    'termsDay': terms_of_days,
                },
                'isClosed': False,
                'canPay': True,
                'inElastic': True,
            },
            response_key='id',
            token=token,
            content_type='application/json',
        )

    async def set_active(
            self,
            token: str,
            uuid: str,
    ):
        return await self.request(
            type_=RequestTypes.POST,
            prefix=f'/{uuid}/send',
            token=token,
        )

    async def set_inactive(
            self,
            token: str,
            uuid: str,
    ):
        return await self.request(
            type_=RequestTypes.POST,
            prefix=f'/{uuid}/cancel',
            token=token,
        )

    async def get_qrcode(
            self,
            token: str,
            uuid: str,
            img_width: int = 174,
            img_height: int = 386,
            get_image: bool = True,
    ):
        return await self.request(
            type_=RequestTypes.GET,
            prefix=f'/{uuid}/qrcode',
            parameters={
                'imgWidth': img_width,
                'imgHeight': img_height,
                'getImage': get_image,
            },
            response_key='result',
            token=token,
        )
