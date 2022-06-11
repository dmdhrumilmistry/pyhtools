#!usr/bin/env python3
import argparse
import scapy.all as sp

def get_args():
    '''
    get arguments if any
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface', help='checks for specific interface')
    
    args = parser.parse_args()
    interface = args.interface
    del parser
    del args
    
    return interface


def get_mac(ip:str):
    '''
    returns mac address of the ip
    '''
    arp_req = sp.ARP(pdst=ip)
    brdcst = sp.Ether(dst='ff:ff:ff:ff:ff:ff')

    packet = brdcst / arp_req
    responded_list = sp.srp(packet, timeout = 1, verbose = False)[0]

    return responded_list[0][1].hwsrc


def check_spoof(packet)->bool:
    '''
    checks if machine is under ARP/MITM attack.
    '''
    
    if packet.haslayer(sp.ARP) and packet[sp.ARP].op == 2:
        try:
            real_mac = get_mac(packet[sp.ARP].psrc)
            response_mac = packet[sp.ARP].hwsrc
            if real_mac != response_mac:
                print(f"[!] ARP Spoof Detected! {response_mac} is imposter. {response_mac} is spoofing as {real_mac}")
        except IndexError:
            pass
    

def capture_packets(iface:str):
    '''
    captures and processes captured packets.
    '''
    sp.sniff(iface=iface, store=False, prn=check_spoof)


INTERFACE = get_args()
capture_packets(INTERFACE)