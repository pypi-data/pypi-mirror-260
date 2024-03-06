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


from addict import Dict
from aiohttp import ClientSession

from ...utils import BaseRoute, RequestTypes


class ClientTokenRoute(BaseRoute):
    async def get(
            self,
            client_id: int,
            client_secret: str,
            service_provider_id: int,
            service_id: int,
    ):
        parameters = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'scope': 'epos.public.invoice',
            'client_secret': client_secret,
            'serviceproviderid': service_provider_id,
            'serviceid': service_id,
            'retailoutletcode': 1,
        }
        json, url_parameters, data = await self.create_data(
            parameters=parameters,
            type_=RequestTypes.POST,
        )

        url = await self.create_url(
            custom_url='https://iii.by/connect/token',
            parameters=url_parameters,
        )

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        async with ClientSession() as session:
            response = await session.post(url=url, data=json, headers=headers)
            response_json = await response.json()

            response = Dict(**response_json)

        return response.get('access_token')
