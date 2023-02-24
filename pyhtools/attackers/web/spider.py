from asyncio import run
from html import unescape
from urllib.parse import urljoin


from pyhtools.UI.colors import BRIGHT_YELLOW
from pyhtools.attackers.web.utils import AsyncRLRequests

import re
import argparse


class Spider:
    def __init__(self, rate_limit:int=100, delay:int=0.0001, headers:dict=None) -> None:
        # list to save links on the whole webpage
        # to avoid repetition
        self.target_links = set()
        self._client = AsyncRLRequests(rate_limit=rate_limit, delay=delay, headers=headers)

    async def get_links(self, url: str) -> list:
        '''
        description: extracts links from the whole webpage.
        params: url(str) of the webpage
        returns: links(list) present in the webpage
        '''
        response = await self._client.request(url=url)
        content = response.get('res_body')
        # TODO: use beautiful soup instead of regex 
        return re.findall(r'(?:href=")(.*?)"', content)

    async def get_target_links(self, url: str, print_link: bool = True):
        '''
        description: extracts useful links and prints them which are
        only related to the target webpage.
        params: links(list) from the target webpage
        returns: useful links(list) related to target webpage
        '''
        # extract links from page
        links:list = await self.get_links(url)

        new_links = set()
        for link in links:
            link = urljoin(url, link)

            if '#' in link:
                link = link.split('#')[0]

            if link not in self.target_links and url in link:
                link = unescape(link)
                self.target_links.add(link)
                new_links.add(link)

                if print_link:
                    print(link)

        return new_links

    async def start(self, target_url:str, print_links: bool = True):
        '''
        description: starts spider
        '''
        queue = [target_url]
        while queue:
            # extract a link from queue
            current_url = queue.pop(0)

            # continue if url is already visited
            if current_url in self.target_links:
                continue

            # add url to visited set
            self.target_links.add(current_url)

            # get links from 
            links = await self.get_target_links(current_url, print_link=print_links)

            # add new links to queue
            queue.extend(self.target_links - links)

        return self.target_links
    

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target_url', required=True,
                        help='url of the target eg: https://example.com')
    args = parser.parse_args()

    target_url = args.target_url
    spider = Spider()
    discovered_links = run(spider.start(target_url=target_url, print_links=True))
    print(f'[*] Total Links Found: {len(discovered_links)-1}')
