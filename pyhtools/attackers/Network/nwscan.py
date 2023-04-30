from pyhtools.UI.colors import BRIGHT_WHITE, BRIGHT_YELLOW, BRIGHT_RED


import scapy.all as sp
import argparse


def get_args():
    '''get arguments from the command line.
    
    Args:
        None

    Returns: 
        str: IP address/range
    '''
    parser = argparse.ArgumentParser(description='search for other devices on the network')
    parser.add_argument('-ip', help='ip or ip range of the target device')
    args = parser.parse_args()

    return args.ip


def scan(ip):
    '''scans ip range for clients and returns discovered clients list.
    
    Args: 
        ip (str): IP address/range of client to be discovered

    Returns: 
        list: IP addresses of discovered network clients  
    '''
    print(BRIGHT_WHITE + f'[*] Discovering Clients {ip}')
    arp_req = sp.ARP(pdst=ip)
    brdcst = sp.Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = brdcst / arp_req
    responded_list = sp.srp(packet, timeout=2, retry=3,verbose=False)[0]

    clients = []
    for ele in responded_list:
        clients.append({"ip": ele[1].psrc, 'mac': ele[1].hwsrc})

    return clients


def print_clients(clients):
    '''prints discovered clients on the network ip range.
    
    Args: 
        clients (list): list of discovered ip addresses

    Returns: 
        None
    '''
    print(BRIGHT_YELLOW + '________________________________________________________')
    print(BRIGHT_YELLOW + 'IP\t\t\tMAC Address')
    print(BRIGHT_YELLOW + '--------------------------------------------------------')

    for client in clients:
        print( BRIGHT_WHITE + client.get('ip') + '\t\t' + client.get('mac'))
    
    print(BRIGHT_YELLOW + '________________________________________________________\n')
    

def run_nwscan(ip:str):
    '''starts network scanner for specified ip range or ip.
    
    Args: 
        ip (str): IP address/range of scan target

    Returns: 
        None
    '''
    try:
        print(BRIGHT_YELLOW + '[*] Starting Network Scanner....')
        clients = scan(ip)
        print_clients(clients)
    except Exception as e:
        print(BRIGHT_RED + '[-] Exception : ', e)


if __name__ == "__main__":
    IP = get_args()
    run_nwscan(IP)
