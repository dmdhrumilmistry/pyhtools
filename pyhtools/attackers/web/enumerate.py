from asyncio import ensure_future, gather, run
from urllib.parse import urljoin
from pyhtools.attackers.web.utils import AsyncRLRequests
from pyhtools.utils import read_file_lines

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


class Discoverer:
    '''
    Discoverer can be used to enumerate directories and subdomains of target website.
    '''

    def __init__(self, *args, **kwargs) -> None:
        self._requester = AsyncRLRequests(*args, **kwargs)

    async def _filter_request(self, url: str, status_codes: list[int] = [200, 403, 500]):
        '''prints url if reponse status code matches code from status_codes.
        
        Args:
            url (str): URL of website   
            status_codes (list): list of integer containing HTTP response  
            status codes, which detects that directory/subdomain exists

        Returns:
            None
        '''
        response = await self._requester.request(url=url)
        
        if isinstance(response, dict) and response.get('status') in status_codes:
            print(url, response.get('status'))

    async def check_dirs(self, domain: str, wordlist_path: str, status_codes: list[int] = [200, 403, 500]):
        '''enumerate website directories

        Args:
            domain (str): domain of the target
            wordlist_path (str): path of wordlist file
            status_codes (list): list of integer containing HTTP response  
            status codes, which detects that directory exists

        Returns:
            None
        '''
        if not domain.endswith('/'):
            domain += '/'
        if not domain.startswith('https://') or domain.startswith('http://'):
            domain = f'http://{domain}'

        dirs = read_file_lines(wordlist_path)

        tasks = []
        for dir in dirs:
            link = urljoin(domain, dir)
            tasks.append(
                ensure_future(
                    self._filter_request(link, status_codes)
                )
            )

        await gather(*tasks)

    async def check_subdomains(self, domain: str, wordlist_path: str, status_codes: list[int] = [200, 403, 500]):
        '''enumerate website subdomains

        Args:
            domain (str): domain of the target
            wordlist_path (str): path of wordlist file
            status_codes (list): list of integer containing HTTP response  
            status codes, which detects that directory exists

        Returns:
            None
        '''
        domain = domain.replace('https://', '').replace('http://', '')
        subdomains = read_file_lines(wordlist_path)

        tasks = []
        for subdomain in subdomains:
            url = f'http://{subdomain}.{domain}'
            tasks.append(
                ensure_future(
                    self._filter_request(url, status_codes)
                )
            )

        await gather(*tasks)
