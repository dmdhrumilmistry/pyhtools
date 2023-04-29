from asyncio.exceptions import CancelledError
from prettytable import PrettyTable
from pyhtools.UI.colors import BRIGHT_RED, BRIGHT_WHITE, BRIGHT_YELLOW, BACK_RED_BRIGHT_YELLOW, RESET_COLORS
from pyhtools.evil_files.malwares.utils import send_mail


import pyfiglet
import os
import sys
import pyhtools.attackers.attackers as attacker
import pyhtools.evil_files.malwares.reverse_backdoor.TCP.listener as listener

__version = '2.1.0'

def clrscr():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')


def banner():
    '''
    prints PyHTools Banner
    '''
    clrscr()
    print(BRIGHT_YELLOW + pyfiglet.figlet_format('PyHTools'))
    print(BRIGHT_YELLOW + '+' + '-'*42 + '+')
    print(BRIGHT_WHITE + f'| written by dmdhrumilmistry\tpht v{__version} |')
    print(BRIGHT_YELLOW + '+' + '-'*42 + '+')


def print_help():
    '''
    prints commands with their brief description.
    '''
    print(BRIGHT_WHITE + 'Python Hacking Tools (PyHTools) (pht)')

    help = PrettyTable(['Command', 'Description'])
    help.align['Command'] = 'c'
    help.align['Description'] = 'l'
    # help.add_row(['',''])

    help.add_row(['clear', 'clear console'])
    help.add_row(['help', 'display help table'])
    help.add_row(['close pht', 'exit PyHackingTools'])

    help.add_row(['machngr', 'change mac address of the network interface'])
    help.add_row(['arpspoofer', 'spoof the target by arp poisoning'])
    help.add_row(['nwscan', 'scan for ip range in the network'])

    help.add_row(
        ['webspider', 'maps all the links which are related to root url on the website'])
    help.add_row(
        ['webcrawldirs', 'scan for valid directories of the website using a wordlist'])
    help.add_row(
        ['webcrawlsubdom', 'scan for valid subdomains of the website using a wordlist'])
    help.add_row(['weblogin', 'bruteforce webpage login'])
    help.add_row(['webvulnscan', 'scan for vulnerabilities on the website'])

    # help.add_row(['',''])

    help.add_row(['listener', 'start listener on specific LHOST and LPORT'])
    help.add_row(['sendmail', 'send mail to specific email address'])

    help.add_row(
        ['gen exe', 'generate executables of reverse backdoor, keylogger, etc.'])

    print(help)


def send_mail_to(email, password, receiver, subject, body) -> bool:
    '''
    send mail
    '''
    print(BRIGHT_WHITE + '[*] Sending email...')
    msg = f'Subject: {subject}\n{body}'
    if send_mail(email, receiver, password, msg):
        print(BRIGHT_YELLOW + '[\u2714] Mail Sent')
    else:
        print(BRIGHT_RED + '[\u274c] Unable to send mail.')


def listener_option():
    '''
    executes commands to run listener option.
    '''
    host = input('[+] LHOST : ')
    port = int(input('[+] LPORT : '))
    lsnr = listener.Listener(host, port)
    lsnr.run()


def sendmail_option():
    '''
    executes commands to run send mail option.
    '''
    email = input('[+] gmail acc : ')
    password = input('[+] password : ')
    print('[!] if you want to send mail to yourself enter "self" (without quotes)')
    receiver = input('[+] email to : ')
    if receiver.lower() == 'self':
        receiver = email
    subject = input('[+] subject : ')
    body = input('[+] body : ')
    send_mail_to(email, password, receiver, subject, body)


def machngr_option():
    '''
    executes commands to change mac address
    '''
    attacker.mac_changer()


def generate_executable():
    '''
    executes commands to generate executables   
    '''
    print(BRIGHT_YELLOW +
          '[-] Currently this feature is under test... Will update soon...')
    print(BRIGHT_WHITE +
          '[*] You can use scripts from malwares to manually generate evil files...')


async def run():
    '''
    start PyHTools
    '''
    try:
        while True:
            cmd = input(BACK_RED_BRIGHT_YELLOW + 'pyhtools >>' +
                        RESET_COLORS + ' ').lower().strip()

            # BASIC UI COMMANDS
            if cmd == 'close pht':
                break

            elif cmd == 'clear':
                clrscr()

            elif cmd == 'help':
                print_help()

            # MALWARES
            elif cmd == 'listener':
                listener_option()

            elif cmd == 'sendmail':
                sendmail_option()

            elif cmd == 'gen exe':
                generate_executable()

            # NETWORK ATTACKERS
            elif cmd == 'machngr':
                machngr_option()

            elif cmd == 'arpspoofer':
                attacker.arpspoofer()

            elif cmd == 'nwscan':
                attacker.nw_scan()

            # WEB ATTACKERS
            elif cmd == 'webspider':
                await attacker.webspider()

            elif cmd == 'webcrawldirs':
                await attacker.webcrawldirs()

            elif cmd == 'webcrawlsubdom':
                await attacker.webcrawlsubdom()

            elif cmd == 'weblogin':
                attacker.brute_login()

            elif cmd == 'webvulnscan':
                attacker.webvulnscan()

            else:
                print(BRIGHT_RED +
                      '[-] Unknown command, use help to view valid commands')

    except (EOFError, KeyboardInterrupt, CancelledError):
        print()
        print(BRIGHT_YELLOW +
              "[\U0001f604] WE ARE NEVER RESPONSIBLE FOR YOUR ACTIONS!")
        print(BRIGHT_RED + '[-] Closing PHT....')
        sys.exit(0)


if __name__ == '__main__':
    banner()
    print(BRIGHT_YELLOW +
          '[\U0001f604] Run pyhtools.py to start Python Hacking Tools.')
