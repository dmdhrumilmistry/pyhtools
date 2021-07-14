#!usr/bin/env python3
from os import name
import requests
import re
from urllib.parse import urljoin
import argparse
from UI.colors import *


# list to save links on the whole webpage
# to avoid repetition
target_links = [] 

def start_spider(target_url):
    '''
    description: starts spider
    '''

    def get_links(url:str)->list:
        '''
        description: extracts links from the whole webpage.
        params: url(str) of the webpage
        returns: links(list) present in the webpage
        '''
        response = requests.get(url)
        content = str(response.content)
        return re.findall(r'(?:href=")(.*?)"',content)


    def get_target_links(url:str):
        '''
        description: extracts useful links and prints them which are
        only related to the target webpage.
        params: links(list) from the target webpage
        returns: useful links(list) related to target webpage
        '''
        global target_links
        links = get_links(url)
        for link in links:
            link = urljoin(url, link)

            if '#' in link:
                link = link.split('#')[0]

            # print(BRIGHT_RED+ link)
            if link not in target_links and target_url in link:
                target_links.append(link)
                print(link)
                get_target_links(link)

    try:
        print(BRIGHT_YELLOW + '[*] Starting SPIDER...')
        get_target_links(target_url)
        print(BRIGHT_YELLOW + f'[*] Mapped all links found on {target_url}')
        print(BRIGHT_YELLOW + "[*] Total Links Found : ", len(target_links))
    except KeyboardInterrupt:
        print(BRIGHT_YELLOW + '\r[!] ctrl+c detected! Exiting Spider.')
    except Exception as e:
        print(BRIGHT_RED + '[-] Exception : ', e)
    finally:
        print(BRIGHT_YELLOW + "[*] Total Links Found Before Exception : ", len(target_links))


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target_url', help='url of the target eg: https://facebook.com, https://github.com, http://bing.com')
    args = parser.parse_args()
    del parser

    target_url = args.target_url
    start_spider(target_url)