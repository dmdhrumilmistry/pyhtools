from argparse import ArgumentParser
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
    def __init__(self, base_url: str, wordlist_path: str, match_codes: list[int], rate_limit: int = 20, delay: float = 0.05, output_file_path: str = None) -> None:
        assert isinstance(base_url, str)
        assert isinstance(wordlist_path, str) and isfile(wordlist_path)

        self.base_url = base_url
        self.wordlist_path = wordlist_path
        self.output_file_path = output_file_path
        self.match_codes = match_codes
        self._delay = delay
        self._semaphore = asyncio.Semaphore(rate_limit)

    async def check_endpoint(self, endpoint: str):
        '''
        description: checks if endpoint is valid or not, returns dict containing endpoint information
        args: endpoint(str): api endpoint
        returns: dict or None
        '''
        assert isinstance(endpoint, str)

        url = urljoin(self.base_url, endpoint)
        async with self._semaphore:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    if response.status in self.match_codes:
                        logger.info(f'{endpoint}\t{response.status}')

                    logger.debug(f'{url}\t{response.status}')

                    res_body = (await response.read()).decode('utf-8')

                    await asyncio.sleep(self._delay)
                    return {
                        "endpoint": endpoint,
                        "status": response.status,
                        "req_url": str(response.request_info.real_url),
                        "req_method": response.request_info.method,
                        "req_headers": dict(response.request_info.headers),
                        "res_headers": dict(response.headers),
                        "res_body": res_body,
                    }

    async def get_endpoints(self):
        '''
        description: returns endpoints from wordlist file
        returns: list
        '''
        endpoints = None
        with open(self.wordlist_path, 'r') as f:
            endpoints = [str(endpoint).strip() for endpoint in f.readlines()]

        return endpoints

    async def save_result_to_file(self, results: list[dict], file_path: str,):
        '''
        description: saves json result to file
        args: results(list of dict)
        returns: bool
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

    async def start(self):
        endpoints = await self.get_endpoints()

        tasks = []
        for endpoint in endpoints:
            tasks.append(
                asyncio.ensure_future(
                    self.check_endpoint(endpoint=endpoint)
                )
            )

        results = await asyncio.gather(*tasks)

        if self.output_file_path:
            await self.save_result_to_file(
                results=results,
                file_path=self.output_file_path,
            )
