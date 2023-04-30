from bs4 import BeautifulSoup
from html import unescape
from urllib.parse import urljoin
from .utils import AsyncRLRequests


class Spider:
    '''
    class Spider used to extract links from website's webpage
    '''
    def __init__(self, rate_limit:int=100, delay:int=0.0001, headers:dict=None) -> None:
        '''
        Spider constructor

        Args:
            rate_limit (int): number of concurrent requests at the same time 
            delay (float): delay between consecutive requests 
            headers (dict): overrides default headers while sending HTTP requests 

        Returns:
            None
        '''
        # list to save links on the whole webpage
        # to avoid repetition
        self.target_links = set()
        self._client = AsyncRLRequests(rate_limit=rate_limit, delay=delay, headers=headers)

    async def get_links(self, url: str) -> set:
        '''extracts links from the whole webpage

        Args: 
            url (str): URL of the webpage

        Returns: 
            list: list of links present in the webpage
        '''
        response = await self._client.request(url=url)
        html = response.get('res_body')
        if html is None:
            return set()
        
        soup = BeautifulSoup(html, 'html.parser')

        href_links = set()
        for link in soup.find_all(href=True):
            href_link = link.get('href')
            if href_link:
                href_links.add(href_link)

        return href_links

    async def get_target_links(self, url: str, print_link: bool = True):
        '''extracts useful links and prints them which are
        only related to the target webpage

        Args: 
            links (list): list of all links from the target webpage

        Returns:
            list: returns useful links list related to target webpage
        '''
        # extract links from page
        links:set = await self.get_links(url)

        new_links = set()
        for link in links:
            link = urljoin(url, link)

            if '#' in link:
                link = link.split('#')[0]

            if link not in self.target_links and url in link:
                link = unescape(link)
                new_links.add(link)

                if print_link:
                    print(link)

        return new_links

    async def start(self, target_url:str, print_links: bool = True):
        '''starts spider

        Args:
            target_url (str): URL of the target website
            print_links (bool): if True prints links found on console
        
        Returns:
            list: list of links found by spider
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

            # skip scraping static files since it'll slow down process
            if current_url.endswith(('.css', '.js','.jpeg', '.png','.svg')):
                continue

            # get links from 
            links = await self.get_target_links(current_url, print_link=print_links)

            # add new links to queue
            queue.extend(links - self.target_links)

        return self.target_links
    
