#!usr/bin/env python3
from UI.colors import BRIGHT_YELLOW
import attackers.Network.arpspoofer as arp
import attackers.Network.nwscan as nwscan

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


if __name__ == "__main__":
    print('[*] Attackers module!. Exiting...')