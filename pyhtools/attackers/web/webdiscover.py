import argparse
import os
import sys
import requests


from pyhtools.UI.colors import *
from threading import Thread


class Discoverer:
    '''
    helps to discover directories, files and subdomains
    '''
    @staticmethod
    def request(url, valid_status_codes: list[int] = None) -> bool:
        '''
        description: requests for specific url and 
        returns true if url is valid.
        params : url(str), status_codes list[int]
        returns : bool
        '''
        if not valid_status_codes:
            status_codes = [200, 204, 301, 302, 307, 401]

        try:
            response = requests.get(url, timeout=0.5)
            if response.status_code in status_codes:
                return True
            return False
        except Exception as e:
            # print(f'{BRIGHT_RED}[-] Request Exception: {e}')
            return False

    @staticmethod
    def __check_subdomain(domain: str, subdomain: str) -> bool:
        '''
        description: checks if subdomain exists under domain. 
        prints generated url and returns True if url is valid
        params: subdomain(str), domain(str) 
        returns: bool
        '''
        url = f'http://{subdomain}.{domain}'

        if Discoverer.request(url):
            print(f'[\u2713] {url}')
            return True
        else:
            return False

    @staticmethod
    def __check_directory(domain: str, dir_name: str) -> bool:
        '''
        description: checks for directory for domain. 
        prints url and returns True if generated url is valid. 
        params: domain(str), dir_name(str)
        returns : bool
        '''
        url = f'http://{domain}/{dir_name}'
        if Discoverer.request(url):
            print(f'[\u2713] {url}')
            return True
        else:
            return False

    @staticmethod
    def check_dirs(domain: str, wordlist: str, ):
        return Discoverer.__perform_function(
            func=Discoverer.__check_directory,
            wordlist=wordlist,
            domain=domain
        )

    @staticmethod
    def check_subdomains(domain: str, wordlist: str):
        return Discoverer.__perform_function(
            func=Discoverer.__check_subdomain,
            wordlist=wordlist,
            domain=domain
        )

    @staticmethod
    def __perform_function(func, wordlist: str, domain: str, threads: int = 5) -> bool:
        '''
        description: performs specific function on passed keyword arguements
        params: func(function), **kwargs(keyword arguments)
        returns: bool
        '''
        # if file does not exists return False
        if not os.path.isfile(wordlist):
            return False

        # load wordlists into a list
        words = ['']
        with open(wordlist, 'r') as wordlist_file:
            words = wordlist_file.readlines()

        # sanitize list
        words = [word.strip() for word in words]

        # function to manage thread
        def manage_thread():
            while len(words) != 0:
                word = words[0]
                func(domain, word)
                words.pop(0)

        # create threads list
        threads_list:list[Thread] = []

        for _ in range(threads):
            thread = Thread(target=manage_thread)
            threads_list.append(thread)

        # start threads
        for thread in threads_list:
            thread.start()

        # stop threads
        for thread in threads_list:
            thread.join()

        return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='webdiscover')
    parser.add_argument('-t', '--target-domain', dest='target_domain',
                        help='domain of your target eg. google.com, bing.com, facebook.com, etc.', required=True)
    parser.add_argument('-w', '--wordlist', dest='wordlist',
                        help='path to wordlist', required=True)
    parser.add_argument('-m', '--mode', dest='mode',
                        help='modes : subdom(find subdomains of the target domain), dir(find directories of the target domain). default mode is `dir`', default='dir')

    args = parser.parse_args()
    target_domain = args.target_domain
    wordlist_file = args.wordlist
    mode = args.mode

    try:
        if mode == 'subdom':
            print(f'{BRIGHT_YELLOW}[1] Finding subdomains')
            Discoverer.check_subdomains(
                domain=target_domain,
                wordlist=wordlist_file
            )

        elif mode == 'dir':
            print(f'{BRIGHT_YELLOW}[2] Finding directories and files')
            Discoverer.check_dirs(
                domain=target_domain,
                wordlist=wordlist_file,
            )

        else:
            print(f'{BRIGHT_RED}[!] invalid mode. Use -h tag to print help.')

    except KeyboardInterrupt or EOFError:
        print('[!] User Interrupted!')
        sys.exit()
