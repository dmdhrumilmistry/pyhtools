#!usr/bin/env python3


import scapy.all as sp
import argparse


parser = argparse.ArgumentParser(description='search for other devices on the network')
parser.add_argument('-ip', help='ip/ip range of the target device')
args = parser.parse_args()

IP = args.ip


def scan(ip):
    arp_req = sp.ARP(pdst=ip)
    brdcst = sp.Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = brdcst / arp_req
    responded_list = sp.srp(packet, timeout=1, verbose=False)[0]

    clients = []
    for ele in responded_list:
        clients.append({"ip": ele[1].psrc, 'mac': ele[1].hwsrc})

    return clients


def print_clients(clients):
    print('________________________________________________________')
    print('IP\t\t\tMAC Address')
    print('--------------------------------------------------------')

    for client in clients:
        print(client.get('ip') + '\t\t' + client.get('mac'))


clients = scan(IP)
print_clients(clients)
