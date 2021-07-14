#!usr/bin/env python3
import kamene.all as sp
import argparse
from UI.colors import *
# from colors import *


def get_args():
    '''
    description: get arguments from the command line.
    params: None
    returns: str
    '''
    parser = argparse.ArgumentParser(description='search for other devices on the network')
    parser.add_argument('-ip', help='ip or ip range of the target device')
    args = parser.parse_args()

    return args.ip


def scan(ip):
    '''
    description: scans ip range for clients and returns discovered clients list.
    params: ip (str)
    returns: clients (list)
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
    '''
    description: prints discovered clients on the network ip range.
    params: clients(list)
    returns: None
    '''
    print(BRIGHT_YELLOW + '________________________________________________________')
    print(BRIGHT_YELLOW + 'IP\t\t\tMAC Address')
    print(BRIGHT_YELLOW + '--------------------------------------------------------')

    for client in clients:
        print( BRIGHT_WHITE + client.get('ip') + '\t\t' + client.get('mac'))
    
    print(BRIGHT_YELLOW + '________________________________________________________\n')
    

def run_nwscan(IP:str):
    '''
    description: starts network scanner for specified ip range or ip.
    params: IP (str)
    returns: None
    '''
    try:
        print(BRIGHT_YELLOW + '[*] Starting Network Scanner....')
        clients = scan(IP)
        print_clients(clients)
    except Exception as e:
        print(BRIGHT_RED + '[-] Exception : ', e)


if __name__ == "__main__":
    IP = get_args()
    run_nwscan(IP)
