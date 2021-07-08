#!usr/bin/env python3

from vuln_scanner.colors import BRIGHT_YELLOW
import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from colors import *


class Scanner:
    def __init__(self, url:str, ignore_links:list) -> None:
        self.target_url = url
        self.ignore_links = ignore_links
        
        self.session = requests.Session()
        self.target_links = []


    def get_links(self, url:str)->list:
        '''
        description: extracts links from the whole webpage.
        params: url(str) of the webpage
        returns: links(list) present in the webpage
        '''
        response = self.session.get(url)
        content = str(response.content)
        return re.findall(r'(?:href=")(.*?)"',content)


    def get_target_links(self, url:str):
        '''
        description: extracts useful links and prints them which are
        only related to the target webpage.
        params: links(list) from the target webpage
        returns: useful links(list) related to target webpage
        '''
        links = self.get_links(url)
        for link in links:
            link = urljoin(url, link)

            if '#' in link:
                link = link.split('#')[0]

            # print(BRIGHT_RED+ link)
            if link not in self.target_links and self.target_url in link and link not in self.ignore_links:
                self.target_links.append(link)
                print(link)
                self.get_target_links(link)
    

    def remove_escape_seq(self, content:str)->str:
        r'''
        desc: removes \r \t \n from the html parsed content if present.
        params: content(str)
        returns: str
        '''
        return content.replace(r'\n','').replace(r'\t','').replace(r'\r','')


    def get_page_content(self, url:str):
        '''
        desc: extracts html code of the webpage.
        params: url(str)
        returns: str
        '''
        response = self.session.get(url)
        content = str(response.content)
        content = self.remove_escape_seq(content)
        return content


    def get_forms(self, url:str)->list:
        '''
        description: extracts all the forms on the url webpage.
        params: url(str)
        returns: forms(list)
        ''' 
        page_content = self.get_page_content(url)
        page_content = self.remove_escape_seq(page_content)
        page_html = BeautifulSoup(page_content,'html.parser')
        return page_html.find_all(name='form')


    def submit_form(self, form, value, url):
        '''
        description: submits form with passed value to url passed
        params: form, value, url
        returns: contents of the reponse.
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
        
    
    def run(self):
        '''
        Starts the scanner.
        '''
        # self.get_target_links(self.target_url)
        # forms = self.get_forms(self.target_url)
        
        # response = self.submit_form(forms[0], 'helloTester', 'http://10.0.2.30/dvwa/vulnerabilities/xss_r/')
        # print(response)
        for link in self.target_links:
            forms = self.get_forms(link)
            for form in forms:
                print(BRIGHT_YELLOW + '[*] Scanning/Testing : ', link)

            if "=" in link:
                print(BRIGHT_YELLOW + "[*] Scanning/Testing : ", link)