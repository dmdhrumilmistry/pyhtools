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
        description: checks if endpoint is valid or not
        '''
        assert isinstance(endpoint, str)

        url = urljoin(self.base_url, endpoint)
        async with self._semaphore:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    if response.status in self.match_codes:
                        logger.info(f'{endpoint}\t{response.status}')

                    logger.debug(f'{url}\t{response.status}')

                    res_headers = {}
                    for header_key in response.headers.keys():
                        res_headers[header_key] = response.headers.get(
                            header_key)

                    res_body = (await response.read()).decode('utf-8')

                    await asyncio.sleep(self._delay)
                    return {
                        "endpoint": endpoint,
                        "status": response.status,
                        "res_headers": res_headers,
                        "res_body": res_body,
                    }

    async def get_endpoints(self):
        endpoints = None
        with open(self.wordlist_path, 'r') as f:
            endpoints = [str(endpoint).strip() for endpoint in f.readlines()]

        return endpoints

    async def save_result_to_file(self, results: list[dict], file_path: str,):
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


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-u', '--url', dest='url', required=True,
                        help='base url of web application API')
    parser.add_argument('-w', '--wordlist', dest='wordlist_path',
                        required=True, help='endpoints wordlist file path')
    parser.add_argument('-rl', '--rate-limit', dest='rate_limit', type=int,
                        default=20, help='number of requests to send concurrently during enumeration')
    parser.add_argument('-d', '--delay', dest='delay', type=float,
                        default=0.05, help='delay between requests in seconds')
    parser.add_argument('-mc', '--match-codes', dest='match_codes',
                        nargs='+', type=int, default=[200, 301, 401, 403, 405], help='display or save api endpoints only matching provided http response status codes')
    parser.add_argument('-o', '--output-file', dest='output_file_path', type=str,
                        help='saves results in json format to provided output file path', required=False, default=None)

    args = parser.parse_args()

    discoverer = APIdiscover(
        base_url=args.url,
        wordlist_path=args.wordlist_path,
        match_codes=args.match_codes,
        rate_limit=args.rate_limit,
        delay=args.delay,
        output_file_path=args.output_file_path,
    )

    asyncio.run(
        discoverer.start()
    )
