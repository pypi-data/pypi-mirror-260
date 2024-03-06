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


from io import BufferedReader

from addict import Dict
from aiohttp import ClientSession, ContentTypeError
from furl import furl


class RequestTypes:
    GET = 'get'
    POST = 'post'


class BaseRoute:
    url: str = ''
    prefix: str = ''

    def __init__(self, url: str = None):
        if not url:
            return

        self.url = url + self.prefix
        for i in dir(self):
            if issubclass(eval(f'type(self.{i})'), BaseRoute):
                route: BaseRoute = eval(f'self.{i}')
                route.__init__(url=self.url)

    async def create_url(self, parameters: dict, custom_url: str = None, prefix: str = None) -> str:
        if custom_url:
            f = furl(url=custom_url)
        else:
            f = furl(url=self.url + prefix)
        f.set(args=parameters)
        return f.url

    @staticmethod
    async def create_data(parameters, type_):
        parameters = parameters or {}

        json = {}
        url_parameters = {}
        data = {}

        have_data = False
        for pk, pv in parameters.items():
            if isinstance(pv, BufferedReader):
                have_data = True
                data[pk] = pv
                continue

            url_parameters[pk] = pv

        if type_ == RequestTypes.POST and not have_data:
            json = url_parameters
            url_parameters = {}

        return json, url_parameters, data

    async def request(
            self,
            token: str,
            type_: str = RequestTypes.GET,
            prefix: str = '/',
            parameters: dict = None,
            response_key: str = None,
            content_type: str = None,
    ):
        json, url_parameters, data = await self.create_data(
            parameters=parameters,
            type_=type_,
        )

        url = await self.create_url(
            prefix=prefix,
            parameters=url_parameters,
        )
        headers = {}

        if content_type:
            headers['Content-Type'] = content_type
        headers['Authorization'] = f'Bearer {token}'

        async with ClientSession() as session:
            if type_ == RequestTypes.GET:
                response = await session.get(url=url, headers=headers)
            elif type_ == RequestTypes.POST and url_parameters:
                response = await session.post(url=url, data=data, headers=headers)
            elif type_ == RequestTypes.POST:
                response = await session.post(url=url, json=json, headers=headers)
            try:
                response_json = await response.json()
                if isinstance(response_json, list):
                    response = Dict(**response_json[0])
                else:
                    response = Dict(**response_json)
            except ContentTypeError:
                return response

        if response_key:
            response_new = response.get(response_key)
            if not response_new:
                return response
            else:
                response = response_new
        return response
