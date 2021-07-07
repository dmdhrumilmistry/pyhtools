#!usr/bin/env python3
import requests
import re
from urllib.parse import *


def get_links(url:str)->list:
    '''
    description: extracts links from the whole webpage.
    params: url(str) of the webpage
    returns: links(list) present in the webpage
    '''
    response = requests.get(url)
    content = str(response.content)
    return re.findall(r'(?:href=")(.*?)"',content)


def get_target_links(url:str,links:list):
    '''
    description: extracts useful links and prints them which are
    only related to the target webpage.
    params: links(list) from the target webpage
    returns: useful links(list) related to target webpage
    '''
    target_links = []

    for link in links:
        link = urljoin(url, link)
        
        if link[-1] == '/':
            link = link.rstrip(link[-1])

        if '#' in link:
            link = link.split('#')[0]

        if link not in target_links and url in link:
            target_links.append(link)
            print(link)

    return target_links


def map_urls(url:str)->list:
    '''
    description: maps all the url within the webpage.
    params: target_url
    returns: mapped urls of the webpage
    '''
    links = get_links(url)
    target_links = get_target_links(url,links)
    return target_links


def crawl_website(target_url:str)->None:
    '''
    description: crawls through website and maps all the links.
    params: target_url(str)
    returns: None
    '''
    links = map_urls(target_url)
    for link in links:
        map_urls(link)
    

try:
    target_url = 'https://target_domain.com'
    crawl_website(target_url)
except KeyboardInterrupt:
    print('\r[!] ctrl+c detected! Exiting Spider.')