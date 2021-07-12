#!usr/bin/env python3
import kamene.all as sp
import argparse
from colors import *




def scan(ip):
    print(BRIGHT_WHITE + f'[*] Discovering Clients {IP}')
    arp_req = sp.ARP(pdst=ip)
    brdcst = sp.Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = brdcst / arp_req
    responded_list = sp.srp(packet, timeout=2, retry=3,verbose=False)[0]

    clients = []
    for ele in responded_list:
        clients.append({"ip": ele[1].psrc, 'mac': ele[1].hwsrc})

    return clients


def print_clients(clients):
    print(BRIGHT_YELLOW + '________________________________________________________')
    print(BRIGHT_YELLOW + 'IP\t\t\tMAC Address')
    print(BRIGHT_YELLOW + '--------------------------------------------------------')

    for client in clients:
        print( BRIGHT_WHITE + client.get('ip') + '\t\t' + client.get('mac'))
    
    print(BRIGHT_YELLOW + '________________________________________________________\n')
    


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='search for other devices on the network')
        parser.add_argument('-ip', help='ip or ip range of the target device')
        args = parser.parse_args()

        IP = args.ip
        print(BRIGHT_YELLOW + '[*] Starting Network Scanner....')
        clients = scan(IP)
        print_clients(clients)
    except Exception as e:
        print(BRIGHT_RED + '[-] Exception : ', e)