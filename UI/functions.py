import pyfiglet
import os
import sys
from prettytable import PrettyTable
import threading
# ------------- Custom imports -----------------------
from UI.colors import *
import malwares.reverse_backdoor.listener as listener


def clrscr():
    if os.name=='nt':
        os.system('cls')
    elif os.name=='posix':
        os.system('clear')


def banner():
    '''
    prints PyHTools Banner
    '''
    clrscr()
    print(BRIGHT_YELLOW + '_'*42)
    print(BRIGHT_YELLOW + pyfiglet.figlet_format('PyHTools'))
    print(BRIGHT_YELLOW +'-'*42)
    
    print(BRIGHT_WHITE +'written by Dhrumil Mistry\tpht v1.0')
    print(BRIGHT_YELLOW + '-'*42)


def print_help():
    '''
    prints commands with their brief description.
    '''
    print(BRIGHT_WHITE + 'Python Hacking Tools (PyHTools) (pht)')
    
    help = PrettyTable()
    help.field_names = ['Command','Description']
    help.add_row('arpspoofer','spoof the target by arp poisoning.')
    
    print(help)


def run():
    '''
    start PyHTools
    '''
    wanna_run = True
    while wanna_run:
        cmd = input(BACK_RED_BRIGHT_YELLOW + 'pyhtools >>' + RESET_COLORS + ' ').lower().strip()
        if cmd == 'close pht':
            sys.exit()
        if cmd == 'clear':
            clrscr()
        elif cmd == 'help':
            print_help()
        elif cmd == 'listener':
            host = input('[+] LHOST : ')
            port = int(input('[+] LPORT : '))
            lsnr = listener.Listener(host,port)
            lsnr.run()
