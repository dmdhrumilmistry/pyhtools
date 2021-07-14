from colorama import init, Style, Fore, Back
import pyfiglet

init(autoreset=True)
RESET_COLORS = Style.RESET_ALL

BRIGHT_RED = Style.BRIGHT + Fore.RED
BRIGHT_WHITE = Style.BRIGHT + Fore.WHITE
BRIGHT_YELLOW = Style.BRIGHT + Fore.YELLOW
BACK_RED_BRIGHT_YELLOW = Back.RED + Style.BRIGHT + Fore.YELLOW


def banner():
    '''
    prints PyHTools Banner
    '''
    print(BRIGHT_YELLOW + pyfiglet.figlet_format('PyHTools'))
    print(BRIGHT_YELLOW + '+' +'-'*42 + '+' )
    
    print(BRIGHT_WHITE +'| written by Dhrumil Mistry\tpht v1.0   |')
    print(BRIGHT_YELLOW + '+' + '-'*42 + '+' )


banner()