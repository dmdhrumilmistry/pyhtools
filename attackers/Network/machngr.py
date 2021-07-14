#!usr/bin/env/python3

import subprocess
import re
import argparse
from sys import exit
from random import randint
from UI.colors import *
import os


def get_arguments():
	'''
	description: get arguments from the console.
	params: None
	returns: Interface, new_mac
	'''
	parser = argparse.ArgumentParser(description='Mac Changer')

	parser.add_argument('-i', '--interface', dest='interface',
	                    help='Choose interface')
	parser.add_argument('-m', '--new-mac', dest='new_mac',
	                    help='Choose new mac address or enter random to generate random mac.')
	args = parser.parse_args()

	INTERFACE = args.interface
	NEW_MAC = args.new_mac
	del parser

	if NEW_MAC == 'random':
		print(BRIGHT_WHITE + '[*] Generating Random Mac')
		NEW_MAC = generate_random_mac()

	return INTERFACE, NEW_MAC


def generate_random_mac() -> str:
	'''
	description: generates and returns a random mac address
	params: None
	returns: str
	'''
	rand_mac = '00'
	for _ in range(5):
		rand_mac +=  ':' + format(randint(0,255), 'x')
  
	return rand_mac


def check_args(intrfc, new_mac):
	'''
	decription: checks if args are valid, prints appropriate error and exit.
	Returns True if all parsed arguments are valid. 
	params: interfce(interface), new_mac
	returns: bool
	'''
	if not intrfc:
	    exit(BRIGHT_RED + "[-] Please enter interface argument, use -h or --help for more info")
	elif not new_mac:
	    exit(BRIGHT_RED + "[-] Please enter new mac address as argument, use -h or --help for more info")
	return True


def change_mac(intrfc, new_mac):
    '''
    decription: changes mac address of the interface. returns True if mac changes successfully.
    params: interface, new_mac
    returns: True or exits program.
    '''
    if check_args(intrfc, new_mac):
        try:
            subprocess.call(['sudo', 'ifconfig', intrfc, 'down'])
            subprocess.call(['sudo', 'ifconfig', intrfc, 'hw', 'ether',new_mac])
            subprocess.call(['sudo', 'ifconfig', intrfc, 'up'])
            return True
        
        except Exception as e:
            exit(BRIGHT_RED +'[-] Error occured while changing MAC address')
		

def check_mac_change(intrfc, new_mac, mac_change_status):
	'''
	description: checks if mac address has been changed
  	params: interface, new_mac, mac_change_status
	returns: None
	'''
	if mac_change_status:
	    ifconfig_result = subprocess.check_output(['sudo', 'ifconfig', intrfc])
	    mac_regex = r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w"
	    mac_check_result = re.search(mac_regex, str(ifconfig_result))
	    if mac_check_result:
	        if mac_check_result.group(0) == new_mac:
	            print(BRIGHT_YELLOW + f'[+] {intrfc}  MAC successfully changed\n', BRIGHT_WHITE + f'\r[+] Current Mac: {mac_check_result.group(0)}')
	        else:
	            print(BRIGHT_RED + f"[-] {intrfc} MAC is not changed/ error while reading MAC address please try again")
	            print(BRIGHT_YELLOW + "[+] Current Mac: " + mac_check_result.group(0))
	    else:
	        print(BRIGHT_RED + "[-] MAC not found")


def run_macchanger(interface, new_mac):
	if os.name == 'posix':
		INTERFACE, NEW_MAC = interface, new_mac
		MAC_CHANGE_STATUS = change_mac(INTERFACE, NEW_MAC)
		check_mac_change(INTERFACE, NEW_MAC, MAC_CHANGE_STATUS)
	else:
		print(BRIGHT_RED + "[\U0001f636] Mac changer only works on linux machines with admin privileges.")


if __name__ == '__main__':
	INTERFACE, NEW_MAC = get_arguments()
	run_macchanger(INTERFACE, NEW_MAC)
