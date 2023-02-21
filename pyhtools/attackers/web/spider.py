from urllib.parse import urljoin
from pyhtools.UI.colors import *
from pyhtools.attackers.web.utils import AsyncRLRequests
from asyncio import run


import re
import argparse


class Spider:
    def __init__(self, rate_limit:int=100, delay:int=0.0001, headers:dict=None) -> None:
        # list to save links on the whole webpage
        # to avoid repetition
        self.target_links = []
        self._client = AsyncRLRequests(rate_limit=rate_limit, delay=delay, headers=headers)
        self._tasks = []

    async def get_links(self, url: str) -> list:
        '''
        description: extracts links from the whole webpage.
        params: url(str) of the webpage
        returns: links(list) present in the webpage
        '''
        response = await self._client.request(url=url)
        # TODO: figure out how to extract response body content below 
        # only below line needs change, everything else will remain same.
        # print(response.status, await response.text())
        content = str(response)
        print(content)
        return re.findall(r'(?:href=")(.*?)"', content)

    async def get_target_links(self, url: str, print_link: bool = True):
        '''
        description: extracts useful links and prints them which are
        only related to the target webpage.
        params: links(list) from the target webpage
        returns: useful links(list) related to target webpage
        '''
        target_links = self.target_links
        links = await self.get_links(url)

        for link in links:
            link = urljoin(url, link)

            if '#' in link:
                link = link.split('#')[0]

            if link not in target_links and url in link:
                target_links.append(link)
                if print_link:
                    print(link)
                self.get_target_links(url=link, print_link=print_link)

    async def start(self, target_url:str, print_links: bool = True):
        '''
        description: starts spider
        '''
        # try:
        await self.get_target_links(target_url, print_links)

        # except Exception as e:
            # print(f'{BRIGHT_RED}[!] Exception: {e}')

        # finally:
        return self.target_links


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target_url', required=True,
                        help='url of the target eg: https://facebook.com, https://github.com, http://bing.com')
    args = parser.parse_args()

    target_url = args.target_url
    spider = Spider()
    run(spider.start(target_url=target_url, print_links=True))
    # print(f'[*] Total Links Found: {len(discovered_links)}')
