import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pyhtools.UI.colors import BRIGHT_RED, BRIGHT_WHITE, BRIGHT_YELLOW


class Scanner:
    '''Scans for vulnerabilities in the website'''
    def __init__(self, url:str, ignore_links:list) -> None:

        self.target_url = url
        
        if ignore_links:
            self.ignore_links = ignore_links
        else:
            self.ignore_links = []
        
        self.session = requests.Session()
        self.target_links = []


    def get_links(self, url:str)->list:
        '''extracts links from the whole webpage.
        Args:
            url (str): URL of the webpage
        
        Returns: 
            links (list): list of URLs present in the webpage
        '''
        response = self.session.get(url)
        content = str(response.content)
        return re.findall(r'(?:href=")(.*?)"',content)


    def get_target_links(self, url:str):
        '''extracts useful links and prints them which are
        only related to the target webpage.

        Args:
            links (list):  list of links from the target webpage

        Returns:
            list: useful links as str related to target webpage
        '''
        links = self.get_links(url)
        for link in links:
            link = urljoin(url, link)
            
            if '#' in link:
                link = link.split('#')[0]

            if link not in self.target_links and self.target_url in link and link not in self.ignore_links:
                self.target_links.append(link)
                if requests.get(link).status_code==200:
                    print(link)
                self.get_target_links(link)
    

    def remove_escape_seq(self, content:str)->str:
        r'''removes \r \t \n from the html parsed content if present.
        
        Args: 
            content (str): html page content as string

        Returns: 
            str: escaped html content without \r \t \n chars
        '''
        return content.replace(r'\n','').replace(r'\t','').replace(r'\r','').replace(r"\'","'")


    def get_page_content(self, url:str)->str:
        '''extracts html code of the webpage

        Args:
            url (str): URL of the webpage

        Returns:
            str: Html content as string
        '''
        response = self.session.get(url)
        content = str(response.content)
        content = self.remove_escape_seq(content)
        return content


    def get_forms(self, url:str)->list:
        '''extracts all the forms on the url 
        webpage using beautiful soup 4
        
        Args:
            url (str): URL of webpage

        Returns: 
            list: list of forms (bs4.element.ResultSet)
        ''' 
        page_content = self.get_page_content(url)
        page_content = self.remove_escape_seq(page_content)
        page_html = BeautifulSoup(page_content,'html.parser')
        return page_html.find_all(name='form')


    def submit_form(self, form, value, url):
        '''submits form with passed value to url passed
        
        Args: 
            form (dict): webpage form from bs4.element.ResultSet
            value (str): Form input value to be used while filling form
            url (str): base url of webpage

        Returns: 
            str: html contents of the reponse
        '''
        action = form.get('action')
        post_url = urljoin(url, action)
        # print(post_url)

        method = form.get('method')
        post_data_dict = {}

        inputs = form.find_all('input')
        for input in inputs:
            inp_name = input.get('name') 
            inp_type = input.get('type')
            inp_value = input.get('value')

            if inp_type == 'text':
                inp_value = value

            post_data_dict[inp_name]=inp_value

        if method == 'post':
            post_response = self.session.post(url=post_url, data=post_data_dict)
        else:
            post_response = self.session.get(url=url, params=post_data_dict)
        
        return self.remove_escape_seq(str(post_response.content))
        
    
    def is_xss_vulnerable_in_form(self, form, url)->bool:
        '''tests whether the passed form is xss vulnerable or not. 
        
        Args:
            form (dict): webpage form from bs4.element.ResultSet
            url (str): base url of webpage

        Returns: 
            bool: returns True if vulnerable else False
        '''
        test_script_payload = "<scRipt>alert('vulnerable')</sCript>"
        response_content = self.submit_form(form, test_script_payload, url)
        # response = BeautifulSoup(response_content, 'html.parser')
        # print(BRIGHT_YELLOW + '[-] RESPONSE: \n', response.prettify())
        return test_script_payload in response_content


    def is_xss_vulnerable_in_link(self, url, payload=None):
        '''tests whether the passed url is xss vulnerable or not. 
        
        Args:
            url (str): base url of webpage
            payload (str): XSS payload to be injected in URL during test

        Returns: 
            bool: returns True if vulnerable else False
        '''
        if payload is None:
            payload = "<scRipt>alert('vulnerable')</sCript>"
        url = url.replace('=',f'={payload}')
        response_content = self.get_page_content(url)
        # response = BeautifulSoup(response_content, 'html.parser')
        # print(BRIGHT_YELLOW + '[-] RESPONSE: \n', response.prettify())

        return payload in response_content


    def run(self):
        '''Starts the scanner

        Args:
            None

        Returns: 
            None
        '''
        try:
            try:
                print(BRIGHT_WHITE + '[*] Spider is mapping website.')
                print(BRIGHT_YELLOW + '[!] Press ctrl+c to stop mapping!')
                self.get_target_links(self.target_url)
            except KeyboardInterrupt:
                print(BRIGHT_YELLOW + '\r[!] ctrl+c detected! Stopping Spider. Website mapping stopped.')
            
            print(BRIGHT_WHITE + '[*] Finding vulnerabilites on the mapped webpages.')
            forms = self.get_forms(self.target_url)
            
            for link in self.target_links:
                forms = self.get_forms(link)
                for form in forms:
                    print(BRIGHT_WHITE + '[*] Scanning/Testing vuln in form of link: ', link)
                    if self.is_xss_vulnerable_in_form(form,link):
                        print(BRIGHT_YELLOW + f'[!] Found XSS vuln in {link} form : ')
                        print(form)
                        print()

                if "=" in link:
                    print(BRIGHT_WHITE + '[*] Scanning/Testing vuln from URL of link: ', link)
                    if self.is_xss_vulnerable_in_link(link):
                        print(BRIGHT_YELLOW + '[!] Found XSS vuln in URL :', link)
                        print()
        except Exception as e:
            print(BRIGHT_RED + f'[-] Exception : {e}')