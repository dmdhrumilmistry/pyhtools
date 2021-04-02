#!usr/bin/env/python3


import subprocess
import re
import argparse
from sys import exit

def get_arguments():
	parser = argparse.ArgumentParser(description='Mac Changer')

	parser.add_argument('-i', '--interface', dest = 'interface', help='Choose interface')
	parser.add_argument('-m', '--new-mac', dest = 'new_mac', help='Choose new mac address')
	args = parser.parse_args()

	INTERFACE = args.interface
	NEW_MAC = args.new_mac
	del parser

	return INTERFACE, NEW_MAC

def check_args(intrfc, new_mac):
    if not intrfc:
        exit("[-] Please enter interface argument, use -h or --help for more info")
    elif not new_mac:
        exit("[-] Please enter new mac address as argument, use -h or --help for more info")
    return True


def change_mac(intrfc, new_mac):
	if check_args(intrfc, new_mac):
		try:
			subprocess.call(['sudo', 'ifconfig', intrfc, 'down'])
			subprocess.call(['sudo', 'ifconfig', intrfc, 'hw', 'ether',new_mac])
			subprocess.call(['sudo', 'ifconfig', intrfc, 'up'])
			return True

		except Exception as e:
			exit('[-] Error occured while changing MAC address')
		
	return False


def check_mac_change(intrfc,new_mac, mac_change_status):
	if mac_change_status:
	    ifconfig_result = subprocess.check_output(['sudo', 'ifconfig', intrfc])
	    mac_regex = r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w"
	    mac_check_result = re.search(mac_regex, str(ifconfig_result))
	    if mac_check_result:
	        if mac_check_result.group(0) == new_mac:
	            print("[+] " + intrfc + " MAC successfully changed \n[+] Current Mac: " + mac_check_result.group(0))
	        else:
	            print("[-] " + intrfc + " MAC is not changed/ error while reading MAC address please try again")
	            print("[+] Current Mac: " + mac_check_result.group(0))
	    else:
	        print("[-] MAC not found")


INTERFACE, NEW_MAC = get_arguments()
MAC_CHANGE_STATUS = change_mac(INTERFACE, NEW_MAC)
check_mac_change(INTERFACE, NEW_MAC, MAC_CHANGE_STATUS)
