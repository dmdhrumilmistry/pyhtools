from aiohttp import ClientSession, ClientResponse
from os import name as os_name
from functools import wraps


import asyncio
import aiohttp.resolver

aiohttp.resolver.DefaultResolver = aiohttp.resolver.AsyncResolver
if os_name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class AsyncRequests:
    '''
    AsyncRequests class helps to send HTTP requests.
    '''

    def __init__(self, headers: dict = None) -> None:
        self._headers = headers

    async def request(self, url: str, method: str = 'GET', session: ClientSession = None, *args, **kwargs) -> ClientResponse:
        '''
        Send HTTP requests asynchronously.
        '''
        is_new_session = False
        if not session:
            session = ClientSession(headers=self._headers)
            is_new_session = True

        method = str(method).upper()
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
            if is_new_session:
                await session.close()

        return resp


class AsyncRLRequests(AsyncRequests):
    '''
    Send Asynchronous rate limited HTTP requests.
    '''

    def __init__(self, rate_limit: int = 20, delay: float = 0.05, headers: dict = None) -> None:
        assert isinstance(delay, float) or isinstance(delay, int)
        assert isinstance(rate_limit, float) or isinstance(rate_limit, int)

        self._delay = delay
        self._semaphore = asyncio.Semaphore(rate_limit)
        super().__init__(headers)

    async def request(self, url: str, method: str = 'GET', session: ClientSession = None, *args, **kwargs) -> ClientResponse:
        async with self._semaphore:
            response = super().request(url, method, session, *args, **kwargs)
            await asyncio.sleep(self._delay)
            return response


async def test():
    req = AsyncRLRequests(delay=4)
    res = await asyncio.gather(asyncio.ensure_future(await req.request('https://httpbin.org/get', method='POST')))

    print(type(res), res)

if __name__ == '__main__':
    asyncio.run(test())
