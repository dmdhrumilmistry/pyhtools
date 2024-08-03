from os import name, system

from asyncio.exceptions import CancelledError
from prettytable import PrettyTable
from pyfiglet import figlet_format

from pyhtools_evil_files.malwares.utils import send_mail
from pyhtools_evil_files.malwares.reverse_backdoor.TCP.listener import Listener

from pyhtools.UI.colors import BRIGHT_RED, BRIGHT_WHITE, BRIGHT_YELLOW, RESET_COLORS
# TODO: remove pyhtools/attackers/attackers.py and add it to pyhtools/attackers/__init__.py
from pyhtools.attackers.attackers import (
    mac_changer,
    arpspoofer,
    nw_scan,
    webspider,
    webcrawldirs,
    webcrawlsubdom,
    brute_login,
    webvulnscan,
)


def clrscr():
    '''Clears UI screen

    Args:
        None

    Returns:
        None
    '''
    if name == 'nt':
        system('cls')
    elif name == 'posix':
        system('clear')


def banner():
    '''prints PyHTools Banner on UI Screen

    Args:
        None

    Returns:
        None
    '''
    clrscr()
    print(BRIGHT_YELLOW + figlet_format('PyHTools'))
    print(BRIGHT_YELLOW + '+' + '-'*42 + '+')
    print(BRIGHT_WHITE + '| written by dmdhrumilmistry               |')
    print(BRIGHT_YELLOW + '+' + '-'*42 + '+')


def print_help():
    '''
    prints commands with their brief description.

    Args:
        None

    Returns:
        None
    '''
    print(BRIGHT_WHITE + 'Python Hacking Tools (PyHTools) (pht)')

    help_table = PrettyTable(['Command', 'Description'])
    help_table.align['Command'] = 'c'
    help_table.align['Description'] = 'l'
    # help_table.add_row(['',''])

    help_table.add_row(['clear', 'clear console'])
    help_table.add_row(['help', 'display help_table table'])
    help_table.add_row(['close', 'exit PyHackingTools'])

    help_table.add_row(['machngr', 'change mac address of the network interface'])
    help_table.add_row(['arpspoofer', 'spoof the target by arp poisoning'])
    help_table.add_row(['nwscan', 'scan for ip range in the network'])

    help_table.add_row(
        ['webspider', 'maps all the links which are related to root url on the website'])
    help_table.add_row(
        ['webcrawldirs', 'scan for valid directories of the website using a wordlist'])
    help_table.add_row(
        ['webcrawlsubdom', 'scan for valid subdomains of the website using a wordlist'])
    help_table.add_row(['weblogin', 'bruteforce webpage login'])
    help_table.add_row(['webvulnscan', 'scan for vulnerabilities on the website'])

    # help_table.add_row(['',''])

    help_table.add_row(['listener', 'start reverse TCP listener on specific LHOST and LPORT'])
    help_table.add_row(['sendmail', 'send mail to specific email address'])

    help_table.add_row(
        ['gen exe', 'generate executables of reverse backdoor, keylogger, etc.'])

    print(help_table)


def send_mail_to(email, password, receiver, subject, body) -> bool:
    '''sends mail to receivers

    Args:
        email (str): email of the sender
        password (str): password of sender
        receiver (str): receviever's email address
        subject (str): email subject
        body (str): email text content

    Returns:
        bool: returns True if email was sent successfully, else returns False
    '''
    print(BRIGHT_WHITE + '[*] Sending email...')
    msg = f'Subject: {subject}\n{body}'
    if send_mail(email, receiver, password, msg):
        print(BRIGHT_YELLOW + '[\u2714] Mail Sent')
        return True

    print(BRIGHT_RED + '[\u274c] Unable to send mail.')
    return False


def listener_option():
    '''accepts inputs from user to run reverse TCP backdoor and starts listeners

    Args:
        None

    Returns:
        None
    '''
    host = input('[+] LHOST : ')
    port = int(input('[+] LPORT : '))
    lsnr = Listener(host, port)
    lsnr.run()


def sendmail_option():
    '''Accepts inputs from user to send email

    Args:
        None

    Returns:
        None
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
    '''executes commands to change mac address

    Args:
        None

    Returns:
        None
    '''
    mac_changer()


def generate_executable():
    '''executes commands to generate executables. Work in Progress

    Args:
        None

    Returns:
        None
    '''
    print(BRIGHT_YELLOW +
          '[-] Currently this feature is under test... Will update soon...')
    print(BRIGHT_WHITE +
          '[*] You can use scripts from malwares to manually generate evil files...')


async def run_command(cmd: str):
    # BASIC UI COMMANDS
    match cmd:
        case 'clear':
            clrscr()

        case 'help':
            print_help()

        # MALWARES
        case 'listener':
            listener_option()

        case 'sendmail':
            sendmail_option()

        case 'gen exe':
            generate_executable()

        # NETWORK ATTACKERS
        case 'machngr':
            machngr_option()

        case 'arpspoofer':
            arpspoofer()

        case 'nwscan':
            nw_scan()

        # WEB ATTACKERS
        case 'webspider':
            await webspider()

        case 'webcrawldirs':
            await webcrawldirs()

        case 'webcrawlsubdom':
            await webcrawlsubdom()

        case 'weblogin':
            brute_login()

        case 'webvulnscan':
            webvulnscan()

        case _:
            print(BRIGHT_RED + '[-] Unknown command, use help_table to view valid commands')


async def run():
    '''starts PyHTools UI, interacts with user and executes appropriate 
    functions based on command 

    Args:
        None

    Returns:
        None
    '''
    try:
        while True:
            cmd = input(BRIGHT_RED + 'pyhtools >>' + RESET_COLORS + ' ').lower().strip()
            if cmd == 'close':
                break
            await run_command(cmd)

    except (EOFError, KeyboardInterrupt, CancelledError):
        print()
        print(BRIGHT_YELLOW +
              "[\U0001f604] WE ARE NEVER RESPONSIBLE FOR YOUR ACTIONS!")
        print(BRIGHT_RED + '[-] Closing PHT....')
        exit(0)


if __name__ == '__main__':
    banner()
    print(BRIGHT_YELLOW +
          '[\U0001f604] Run pyhtools.py to start Python Hacking Tools.')
