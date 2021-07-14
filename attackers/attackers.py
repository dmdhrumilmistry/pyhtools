#!usr/bin/env python3
from UI.colors import *
import attackers.Network.arpspoofer as arp
import attackers.Network.nwscan as nwscan
import attackers.Network.machngr as machngr


def arpspoofer():
    '''
    perform arp poisoning attack.
    '''
    target_ip = input('[+] TARGET IP : ')
    spoof_ip = input('[+] SPOOF IP : ')
    perform_mitm = input('[+] Perform MITM attack (y/n)(default=y): ').lower()
    if perform_mitm == 'n':
        perform_mitm = False
    else:
        perform_mitm = True
    arp.run_spoofer(target_ip, spoof_ip, perform_mitm)


def nw_scan():
    '''
    perform network scan.
    '''
    ip_range = input('[+] IP RANGE : ')
    nwscan.run_nwscan(ip_range)


def mac_changer():
    '''
    changes mac of network interface.
    '''
    interface = input('[+] Interface : ')
    print(BRIGHT_YELLOW + '[!] To generate random mac enter "random" (without quotes)')
    new_mac = input('[+] New Mac : ')
    if new_mac == 'random':
        print(BRIGHT_WHITE + '[*] Generating Random Mac')
        new_mac = machngr.generate_random_mac()
    
    machngr.run_macchanger(interface, new_mac)


if __name__ == "__main__":
    print('[*] Attackers module!. Exiting...')