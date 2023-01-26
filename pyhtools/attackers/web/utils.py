from aiohttp import ClientSession, ClientResponse
from os.path import isfile
from urllib.parse import urljoin
from os import name as os_name
from functools import wraps


import asyncio
import aiohttp.resolver
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')

aiohttp.resolver.DefaultResolver = aiohttp.resolver.AsyncResolver
if os_name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class AsyncRequests:
    def __init__(self, rate_limit: int = 20, delay: float = 0.05, headers: dict = None) -> None:
        assert isinstance(rate_limit, int)
        assert isinstance(delay, float)

        self._delay = delay
        self._semaphore = asyncio.Semaphore(rate_limit)
        self._headers = headers

    async def rate_limit(self, request_func:function):
            @wraps(request_func)
            async def wrapper(url, *args, **kwargs):
                async with self._semaphore:
                    async with ClientSession() as session:
                        payload = request_func(session, url, *args, **kwargs)
                        await asyncio.sleep(self._delay)
                        return payload
            return wrapper


    async def request(self, session:ClientSession, method:str, url:str, *args, **kwargs):
        match method:
            case 'GET':
                sent_req = session.get(url, *args, **kwargs)
            case 'POST':
                sent_req = session.post(url, *args, **kwargs)
            case 'PUT':
                sent_req = session.put(url, *args, **kwargs)
            case 'PATCH':
                sent_req = session.patch(url, *args, **kwargs)
            case 'HEAD':
                sent_req = session.head(url, *args, **kwargs)
            case 'OPTIONS':
                sent_req = session.options(url, *args, **kwargs)
            case 'DELETE':
                sent_req = session.delete(url, *args, **kwargs)
            
        async with sent_req as resp:
            return resp
