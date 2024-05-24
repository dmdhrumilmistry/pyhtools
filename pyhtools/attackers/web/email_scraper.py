from collections import deque
from urllib import parse
import requests, re, lxml
from requests import exceptions
from bs4 import BeautifulSoup
from datetime import date
from pyhtools.UI.colors import BRIGHT_RED, BRIGHT_WHITE, BRIGHT_YELLOW
    
class EmailScraper:
    '''
    EmailScraper class scrapes web for real email addresses based on user-specified URL.
    
    Args:
        url (str): url used to scrape emails from web.
        count (int): number of emails user wants scraper to find.
    
    Methods:
        scrape: scrapes emails based on url argument.
        export: exports a .txt file containing scrape results.
    '''
    
    def __init__(self):
        self.USER_URL = None
        self.USER_COUNT = 0
        self.COUNT = 0
        self.URLS = deque([self.USER_URL])
        self.SCRAPPED_URLS = set()
        self.EMAILS = set()
    
    def scrape(self):
        '''
        Scrape web for emails, then asks user if they want to export to text file.
        
        Returns:
            set: returns set of scrapped emails.
        '''
        
        try:
            while len(self.URLS):
                self.COUNT += 1
                if self.COUNT == (self.USER_COUNT+1):
                    break
                url = self.URLS.popleft()
                self.SCRAPPED_URLS.add(url)
        
                parts = parse.urlsplit(url)
                base_url = '{0.scheme}://{0.netloc}'.format(parts)
                path = url[:url.rfind('/')+1] if '/' in parts.path else url
        
                print(BRIGHT_WHITE + '[%d] Processing %s' % (self.COUNT, url))
        
                try:
                    response = requests.get(url)
                except (exceptions.MissingSchema, exceptions.ConnectionError):
                    continue
        
                new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', response.text, re.I))
                self.EMAILS.update(new_emails)
        
                soup = BeautifulSoup(response.text, features='lxml')
        
                for anchor in soup.find_all('a'):
                    link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                    if link.startswith('/'):
                        link = base_url + link
                    elif not link.startswith('http'):
                        link = path + link
                    if not link in self.URLS and not link in self.SCRAPPED_URLS:
                        self.URLS.append(link)
                        
        except KeyboardInterrupt:
            print(BRIGHT_YELLOW + '[-] Closing Program')
            
        if (self.EMAILS):
            print(BRIGHT_WHITE + '[!] Emails Found!')
            for addr in (self.EMAILS):
                print(addr)
            export_choice = str(input('Export scrapped emails to text doc? (Y/N)'))
            if export_choice == 'Y':
                self.export()
            else:
                pass
        else:
             print(BRIGHT_RED + '[-] No Emails Found.')
       
    def export(self, path):
        '''
        Export emails to a .txt file and save in user-specified directory.

        Args:
            path (str): path to directory user wants to save emails file inside.

        Returns:
            .txt file: exports text file containing emails.
        '''
        
        with open(file=str(path) + f'scraped_emails_{date.today()}.txt', mode='w+', encoding='utf-8') as f:
            f.write(f'Emails Scrapped from {self.USER_URL} on {date.today()}\n')
            for addr in self.EMAILS:
                f.write(addr + '\n')
            f.close()