from asyncio import run
from pyhtools.UI.colors import BRIGHT_YELLOW, BRIGHT_WHITE
from pyhtools.attackers.web.vuln_scanner.scanner import Scanner
from pyhtools.attackers.web.spider import Spider
from pyhtools.attackers.web.enumerate import Discoverer


import json
import pyhtools.attackers.Network.arpspoofer as arp
import pyhtools.attackers.Network.nwscan as nwscan
import pyhtools.attackers.Network.machngr as machngr
import pyhtools.attackers.web.login_guesser as web_login


# Use args/kwargs to rate limit requests
discoverer = Discoverer()

# NETWORK ATTACKS
# TODO: Create functions for Network Attackers : codeinjector, dnsspoofer, download replacer, packet_sniffer.
def arpspoofer():
    '''
    description: perform arp poisoning attack.
    params: None
    returns: None
    '''
    target_ip = input('[+] TARGET IP : ')
    spoof_ip = input('[+] SPOOF IP : ')
    perform_mitm = input('[+] Perform MITM attack (y/n)(default=y): ').lower()
    if perform_mitm == 'n':
        perform_mitm = False
    else:
        perform_mitm = True
    arp.run_spoofer(target_ip, spoof_ip, perform_mitm)


def nw_scan():
    '''
    description: perform network scan.
    params: None
    returns: None
    '''
    ip_range = input('[+] IP (192.168.10.1/24): ')
    nwscan.run_nwscan(ip_range)


def mac_changer():
    '''
    description: changes mac of network interface.
    params: None
    returns: None
    '''
    interface = input('[+] Interface : ')
    print(BRIGHT_YELLOW +
          '[!] To generate random mac enter "random" (without quotes)')
    new_mac = input('[+] New Mac : ')
    if new_mac == 'random':
        print(BRIGHT_WHITE + '[*] Generating Random Mac')
        new_mac = machngr.generate_random_mac()

    machngr.run_macchanger(interface, new_mac)


# WEBSITE ATTACKS
# TODO: Create functions for Website Attackers : getform
def brute_login():
    '''
    description: bruteforce website login page.
    params: None
    returns: None
    '''
    target_url = input('[+] TARGET URL : ')
    wordlist_file = input('[+] WORDLIST PATH : ')
    print(BRIGHT_YELLOW +
          '[!] Enter string in post values, eg. {"username":"admin", "password":"", "Login":"submit"} (inspect element in your webbrowser)')
    post_data = input('[+] POST VALUES : ').strip()
    post_values = json.loads(post_data)

    web_login.bruteforce_login(target_url, wordlist_file, post_values)


def webvulnscan():
    '''
    description: scans for vulnerabilities in the website
    params: None
    returns: None
    '''
    target_url = input('[+] TARGET URL : ')

    print(BRIGHT_YELLOW +
          '[!] Enter links to be ignored separated by commas(,)')
    ignore_links = input('[+] IGNORE LINKS : ')

    ignore_links = [link.strip() for link in ignore_links.split(',')]

    vuln_scanner = Scanner(target_url, ignore_links)

    auth_required = input(
        '[+] AUTH REQUIRED? (y/n) (default=n): ').lower().strip()
    login_link = ''
    login_post_values = ''
    if auth_required == 'y':
        login_link = input('[+] LOGIN LINK : ')
        print(BRIGHT_YELLOW +
              "[!] Enter login post values, eg: {'username':'yourusername', 'password':'yourpassword', 'login':'submit'}")
        print(BRIGHT_WHITE +
              '[!] Inspect element in webbrowser to extract values, they might vary for every website.')
        login_post_values = input('[+] LOGIN POST VALUES : ')
        login_post_values = json.loads(login_post_values)

        vuln_scanner.session.post(login_link, data=login_post_values)

    vuln_scanner.run()


async def webspider():
    '''
    description: maps all the links related to the root url
    params: None
    returns: None
    '''
    target_url = input('[+] TARGET URL : ')
    spider = Spider()

    print(f'{BRIGHT_YELLOW}[*] Starting Spider... Press Ctrl+C to interrupt')
    discovered_links = await spider.start(
        target_url=target_url,
        print_links=True
    )
    print(f'[*] Total Links Found: {len(discovered_links)}')


async def webcrawldirs():
    '''
    description: find valid directories of the website using a wordlist
    params: None
    returns: None
    '''
    domain = input('[+] DOMAIN (duckduckgo.com): ')
    wordlist_path = input('[+] WORDLIST PATH: ')
    await discoverer.check_dirs(domain=domain, wordlist_path=wordlist_path)


async def webcrawlsubdom():
    '''
    description: find valid subdomains of the website using a wordlist
    params: None
    returns: None
    '''
    domain = input('[+] DOMAIN (duckduckgo.com) : ')
    wordlist_path = input('[+] WORDLIST PATH : ')
    await discoverer.check_subdomains(domain=domain, wordlist_path=wordlist_path)
