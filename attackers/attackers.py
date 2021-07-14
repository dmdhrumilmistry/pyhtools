#!usr/bin/env python3
from UI.colors import BRIGHT_YELLOW
import attackers.Network.arpspoofer as arp


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


if __name__ == "__main__":
    arpspoofer()