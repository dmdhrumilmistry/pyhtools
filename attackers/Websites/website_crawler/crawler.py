import requests
import os
import argparse
import sys
from UI.colors import *


def get_args()->dict:
    '''
    description: creates a ArgumentParser object collects 
    arguments and returns arguments as a dict
    params: None
    returns: dict 
    '''
    parser = argparse.ArgumentParser() 
    parser.add_argument('-t', '--target-domain', dest='target_domain', help='domain of your target eg. google.com, bing.com, facebook.com, etc.')
    parser.add_argument('-w', '--wordlist', dest='wordlist', help='path to wordlist')
    parser.add_argument('-m','--mode', dest='mode', help='modes : subdomain(find subdomains of the target domain), dirs(find directories of the target domain), subdir (find subdomain and directories of the target domain).')

    args = parser.parse_args()
    del parser
    
    args_dict = {
        'mode' : args.mode,
        'wordlist' : args.wordlist,
        'target_domain':args.target_domain
    }

    return args_dict


def request(url)->bool:
    '''
    description: requests for specific url and 
    returns true if url is valid.
    params : url(str)
    returns : bool
    '''
    try:
        response = requests.get(url, timeout=0.5)
        # print(url)
        # print(response)
        if response.status_code == 200:
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False
    except UnicodeError:
        return False
    except Exception as e:
        print(BRIGHT_RED + '[-] Request Exception : ', e)
        return False


def check_subdomain(domain:str, subdomain:str)->bool:
    '''
    description: checks if subdomain exists under domain. 
    prints generated url and returns True if url is valid
    params: subdomain(str), domain(str) 
    returns: bool
    '''
    url = f'http://{subdomain}.{domain}'
    # print(url)
    if request(url):
        print('[*] Valid Subdomain : ', url)
        return True
    else:
        return False
    

def check_directories(domain:str, dir_name:str)->bool:
    '''
    description: checks for directory for domain. 
    prints url and returns True if generated url is valid. 
    params: domain(str), dir_name(str)
    returns : bool
    '''
    url = f'http://{domain}/{dir_name}'

    if request(url):
        print('[*] Valid Directory : ', url)
    else:
        return False


def perform_function(func, wordlist:str, domain:str)->bool:
    '''
    description: performs specific function on passed keyword arguements
    params: func(function), **kwargs(keyword arguments)
    returns: bool
    '''
    try:
        print(BRIGHT_WHITE + '[*] Loading wordlists...')

        print('='*25)
        if os.path.isfile(wordlist):
            with open(wordlist, 'r') as wordlist_file:
                for word in wordlist_file:
                    word = word.strip()
                    # print(word)
                    func(domain, word)
        else:
            print(BRIGHT_RED + '[-] Wordlist Not Found.')
            print('='*25)
            print(BRIGHT_YELLOW + '[*] Process Completed.')

    except Exception as e:
        print(BRIGHT_RED + '[-] Perform Exception : ', e)
        print(BRIGHT_RED + '[!] Process Interrupted!')


# ========== Main ===============
if __name__ == '__main__':
    print(BRIGHT_YELLOW + '[*] Starting crawler...')

    args = get_args()
    # print(args)

    wordlist_file = r'{}'.format(args['wordlist'])
    target_domain = args['target_domain']

    try:
        if args['mode'] == 'subdomain':
            print(BRIGHT_YELLOW + '[1] Finding subdomains')
            perform_function(check_subdomain, wordlist_file, target_domain)
        elif args['mode'] == 'dirs':
            print(BRIGHT_YELLOW + '[2] Finding directories and files')
            perform_function(check_directories, wordlist_file, target_domain)
        elif args['mode'] == 'subdirs':
            print(BRIGHT_YELLOW + '[1] Finding subdomains')
            perform_function(check_subdomain, wordlist_file, target_domain)
            
            print(BRIGHT_YELLOW + '[2] Finding directories and files')
            perform_function(check_directories, wordlist_file, target_domain)
        else:
            print(BRIGHT_RED + '[-] Unkown mode: use --help or -h for help')
    except KeyboardInterrupt:
        print('[!] ctrl+c detected! Exiting Program..')
        sys.exit()