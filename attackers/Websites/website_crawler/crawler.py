import requests
import os
from colorama import init, Style, Fore 


init(autoreset=True)
BRIGHT_WHITE = Style.BRIGHT + Fore.WHITE
BRIGHT_YELLOW = Style.BRIGHT + Fore.YELLOW
BRIGHT_RED = Style.BRIGHT + Fore.RED


def check_subdomain(subdomain:str, domain:str)->bool:
    '''
    checks if subdomain exists under domain
    params: subdomain(str), domain(str) 
    returns: bool
    '''
    try:  
        url = f'http://{subdomain}.{domain}'
        response = requests.get(url)
        if response.status_code == 200:
            print(url)
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception as e:
        print(BRIGHT_RED + '[-] Request Exception : ', e)
        return False


def check_directories(domain, dir_name)->bool:
    '''
    checks for directory for domain.
    params: domain(str), dir_name(str)
    returns : bool
    '''


# ========== Main ===============
print(BRIGHT_YELLOW + '[*] Starting crawler...')
wordlist_file = r'D:\GithubRepos\hacking_tools\attackers\Websites\website_crawler\wordlists\test-wordlist.txt'
target_domain = 'google.com'

print(BRIGHT_WHITE + '[*] Loading wordlists...')

print('='*25)
print(BRIGHT_YELLOW + '[*] Valid Subdomains :')
if os.path.isfile(wordlist_file):
    with open(wordlist_file, 'r') as wordlist_file:
        for subdomain in wordlist_file:
            subdomain = subdomain.strip()
            check_subdomain(subdomain, target_domain)
else:
    print(BRIGHT_RED + '[-] Wordlist Not Found.')

print('='*25)
print(BRIGHT_YELLOW + '[*] Process Completed.')