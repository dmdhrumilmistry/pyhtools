from aiohttp import ClientSession
from json import JSONDecodeError, dumps as to_json
from os.path import isfile
from urllib.parse import urljoin
from os import name as os_name


import asyncio
import aiohttp.resolver
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')

aiohttp.resolver.DefaultResolver = aiohttp.resolver.AsyncResolver
if os_name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class APIdiscover:
    def __init__(self, base_url: str, match_codes: list[int], rate_limit: int = 20, delay: float = 0.05, output_file_path: str = None, headers: dict = None) -> None:
        assert isinstance(base_url, str)
        assert isinstance(match_codes, list)
        assert isinstance(rate_limit, int)
        assert isinstance(delay, float)

        self.base_url = base_url
        self.output_file_path = output_file_path
        self.match_codes = match_codes
        self._delay = delay
        self._semaphore = asyncio.Semaphore(rate_limit)
        self._headers = headers

    async def check_endpoint(self, endpoint: str):
        '''
        description: checks if endpoint is valid or not, returns dict containing endpoint information
        args: endpoint(str): api endpoint
        returns: dict or None
        '''
        assert isinstance(endpoint, str)

        url = urljoin(self.base_url, endpoint)
        async with self._semaphore:
            async with ClientSession(headers=self._headers) as session:
                async with session.get(url) as response:
                    if response.status in self.match_codes:
                        logger.info(f'{endpoint}\t{response.status}')

                    logger.debug(f'{url}\t{response.status}')

                    await asyncio.sleep(self._delay)
                    return {
                        "endpoint": endpoint,
                        "status": response.status,
                        "req_url": str(response.request_info.real_url),
                        "req_method": response.request_info.method,
                        "req_headers": dict(**response.request_info.headers),
                        "res_redirection": str(response.history),
                        "res_headers": dict(response.headers),
                        "res_body": (await response.read()).decode('utf-8'),
                    }

    async def get_endpoints_from_file(self, wordlist_path: str):
        '''
        reads endpoints from wordlist file and returns as a list
        '''
        assert isinstance(wordlist_path, str) and isfile(wordlist_path)

        endpoints = None
        with open(wordlist_path, 'r') as f:
            endpoints = [str(endpoint).strip() for endpoint in f.readlines()]

        return endpoints

    async def save_result_to_file(self, results: list[dict], file_path: str,):
        '''
        stores json result to file
        '''
        assert isinstance(results, list)
        assert isinstance(file_path, str)

        save_status = False
        with open(file_path, 'w') as f:
            try:
                f.write(to_json(results))
                save_status = True
                logger.info(f'results stored in {file_path}')
            except JSONDecodeError:
                logger.error(
                    f'Invalid json data, Failed to store data in {file_path}')

        return save_status

    async def start_enum_from_file(self, wordlist_file: str):
        '''
        start endpoint enumeration using wordlist
        '''
        endpoints = await self.get_endpoints_from_file(wordlist_file)

        results = await self.enumerate(endpoints=endpoints)

        if self.output_file_path:
            await self.save_result_to_file(
                results=results,
                file_path=self.output_file_path,
            )

    async def start_enum_id(self, ending_id: int, param_name: str, starting_id: int = 0):
        '''
        starts enumeration based on id in GET request
        '''
        assert isinstance(starting_id, int)
        assert isinstance(ending_id, int)
        assert isinstance(param_name, str)

        endpoints = [f'{self.base_url}{param_name}={id_val}' for id_val in range(starting_id, ending_id)]

        results = await self.enumerate(endpoints=endpoints)

        if self.output_file_path:
            await self.save_result_to_file(
                results=results,
                file_path=self.output_file_path,
            )

    async def enumerate(self, endpoints: list):
        '''
        start API enumeration and return captured responses as list
        '''
        assert isinstance(endpoints, list)

        tasks = []
        for endpoint in endpoints:
            tasks.append(
                asyncio.ensure_future(
                    self.check_endpoint(endpoint=endpoint)
                )
            )

        results = await asyncio.gather(*tasks)
        return results
