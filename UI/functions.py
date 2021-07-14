import pyfiglet
import os
import sys
from prettytable import PrettyTable
# ------------- Custom imports -----------------------
from UI.colors import *
import attackers.attackers as attacker
import malwares.reverse_backdoor.listener as listener
import malwares.send_mail.send_mail as mail


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
    
    help = PrettyTable(['Command','Description'])
    help.align['Command'] = 'c'
    help.align['Description'] = 'l'
    # help.add_row(['',''])
    help.add_row(['clear','clear console'])
    help.add_row(['help','display help table'])
    help.add_row(['close pht','exit PyHackingTools'])
    help.add_row(['listener','start listener on specific LHOST and LPORT'])
    help.add_row(['sendmail','send mail to specific email address'])
    
    help.add_row(['gen exe', 'generate executables of reverse backdoor, keylogger, etc.'])
    help.add_row(['arpspoofer','spoof the target by arp poisoning.'])
    
    print(help)


def send_mail_to(email, password, receiver, subject, body)->bool:
    '''
    send mail
    '''
    print(BRIGHT_WHITE + '[*] Sending email...')
    msg = f'Subject: {subject}\n{body}'
    if mail.send_mail_to(email, receiver, password, msg):
        print(BRIGHT_YELLOW + '[\u2714] Mail Sent')
    else:
        print(BRIGHT_RED + '[\u274c] Unable to send mail.')


def listener_option():
    '''
    executes commands to run listener option.
    '''
    host = input('[+] LHOST : ')
    port = int(input('[+] LPORT : '))
    lsnr = listener.Listener(host,port)
    lsnr.run()


def sendmailoption():
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


def generate_executable():
    '''
    executes commands to generate executables   
    '''
    pass



def run():
    '''
    start PyHTools
    '''
    while True:
        cmd = input(BACK_RED_BRIGHT_YELLOW + 'pyhtools >>' + RESET_COLORS + ' ').lower().strip()
        
        if cmd == 'close pht':
            wanna_run = False
            print(BRIGHT_YELLOW + "[\U0001f604] WE ARE NEVER RESPONSIBLE FOR YOUR ACTIONS!")
            print(BRIGHT_RED + '[-] Closing PHT....')
            sys.exit(0)

        if cmd == 'clear':
            clrscr()
        
        elif cmd == 'help':
            print_help()
        
        elif cmd == 'listener':
            listener_option()
        
        elif cmd == 'sendmail':
            sendmailoption()
        
        elif cmd == 'gen exe':
            generate_executable()
        
        elif cmd == 'arpspoofer':
            attacker.arpspoofer()
        
        elif cmd == 'nwscan':
            attacker.nw_scan()

        else:
            print(BRIGHT_RED + '[-] Unknown command, use help to view valid commands')
            