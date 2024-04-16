from bs4 import BeautifulSoup
import requests, re, lxml
from requests import exceptions
from urllib import parse
from collections import deque
from pyhtools.UI.colors import BRIGHT_RED, BRIGHT_WHITE, BRIGHT_YELLOW

##----------------Author: astralm0nke on GitHub-----------------##
class EmailScraper:
    USER_URL = str(input('[+] Specify Target URL to Scan: '))
    USER_COUNT = int(input('[+] Specify Count Limit: '))
    COUNT = 0
    URLS = deque([USER_URL])
    SCRAPPED_URLS = set()
    EMAILS = set()
    
# Main function to scrape emails
    def scrape(self):
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
             print(BRIGHT_RED + '[-] No Emails Found. Womp-Womp!')

# Export emails to a text document, creates file if not found.        
    def export(self):
        path = str(input('Please specify the path to save file: '))
        from datetime import date
        with open(file=path + f'scraped_emails_{date.today()}.txt', mode='w+') as f:
            f.write(f'Emails Scrapped from {self.USER_URL} on {date.today()}')
            for addr in self.EMAILS:
                f.write(addr)
            f.close()