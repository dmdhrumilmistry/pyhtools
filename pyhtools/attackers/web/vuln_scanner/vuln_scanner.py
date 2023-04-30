import scanner
import argparse
from pyhtools.UI.colors import BRIGHT_RED, BRIGHT_YELLOW
import sys


def get_args():
    '''get arguments from the user and return as dict containing
    target_url, ignore_links, login_link, and login_details
    
    Args:
        None
    
    Returns:
        dict: user arguments
    '''
    parser = argparse.ArgumentParser(description='Web Application Vulnerability Scanner')
    parser.add_argument('-t', '--target-url',dest='target_url',help='root url of the target website', required=True)
    parser.add_argument('-ig', '--ignore-links', dest='ignore_links', help='url of wepages which are to be ignored while scanning/testing for vulnerabilities separated by commas')
    parser.add_argument('-l','--login-link',dest='login_link',help='direct login/authentication link')
    parser.add_argument('-ld', '--login-details', dest='login_details', help='pass login details if authentication required as username,password (separated by comma)')
    args = parser.parse_args()

    
    if args.target_url:
        target_url = args.target_url

    login_link = None
    if args.login_link:
        login_link = args.login_link

    login_details = None
    if args.login_details is not None:
        login_details = [detail.strip() for detail in args.login_details.split(',')]

    ignore_links = None
    if args.ignore_links is not None:
        ignore_links = [link.strip() for link in args.ignore_links.split(',')]

    return {
        "target_url": target_url,
        "ignore_links": ignore_links,
        "login_link": login_link,
        "login_details" : login_details,
    }



if __name__ == '__main__':
    args = get_args()

    TARGET_URL = args['target_url']
    print(BRIGHT_YELLOW + '[*] TARGET URL: ', TARGET_URL)

    IGNORE_LINKS = args['ignore_links']
    print(BRIGHT_YELLOW + '[*] LINKS TO BE IGNORED: ', IGNORE_LINKS)

    authentication_required = False
    if args['login_details'] is not None and args['login_link'] is not None:
        try:
            LOGIN_LINK = args['login_link']
            print(BRIGHT_YELLOW + '[*] LOGIN LINK: ', LOGIN_LINK)

            USERNAME = args['login_details'][0]
            print(BRIGHT_YELLOW +'[*] USERNAME: ', USERNAME)
            
            PASSWORD = args['login_details'][1]
            print(BRIGHT_YELLOW + '[*] PASSWORD: ', PASSWORD)
            
            authentication_required = True
        
        except IndexError:
            print(BRIGHT_RED + '[-] PLEASE PROVIDE ALL THE REQUIRED VALUES.')
            print(BRIGHT_YELLOW + '[*] USE -h or --help for usage.')
            sys.exit()

    print()

    vuln_scanner = scanner.Scanner(TARGET_URL, IGNORE_LINKS)
    if authentication_required:
        login_post_values = {"username":USERNAME, "password":PASSWORD, "Login":"submit"}
        vuln_scanner.session.post(LOGIN_LINK, data=login_post_values)
    vuln_scanner.run()