import scapy.all as sp
from argparse import ArgumentParser


class SpoofDetector:
    '''
    SpoofDetector class to detect Local MITM attacks
    '''

    def __init__(self, interface: str) -> None:
        '''SpoofDetector class constructor
        
        Args:
            interface (str): network interface on which spoofing needs to be detected

        Returns:
            None
        '''
        self.interface = interface


    def get_mac(self, ip: str):
        '''returns mac address of the ip

        Args:
            ip (str): ip address of the string

        Returns:
            str: Mac address of the ip in the network
        '''
        arp_req = sp.ARP(pdst=ip)
        brdcst = sp.Ether(dst='ff:ff:ff:ff:ff:ff')

        packet = brdcst / arp_req
        responded_list = sp.srp(packet, timeout=1, verbose=False)[0]
        
        return str(responded_list[0][1].hwsrc)


    def check_spoof(self, packet) -> bool:
        '''checks if machine is under ARP/MITM attack

        Args:
            packet (scapy.Packet): sniffed scapy packet from the interface

        Returns:
            bool: True if ARP spoofing/poisoning detected else False
        '''
        if packet.haslayer(sp.ARP) and packet[sp.ARP].op == 2:
            try:
                real_mac = self.get_mac(packet[sp.ARP].psrc)
                response_mac = packet[sp.ARP].hwsrc
                if real_mac != response_mac:
                    print(
                        f"[!] ARP Spoof Detected! {response_mac} is imposter. {response_mac} is spoofing as {real_mac}")
            except IndexError:
                pass


    def start(self):
        '''captures and processes packets to check whether network is being attacked or not

        Args:
            None:

        Returns:
            None
        '''
        sp.sniff(iface=self.interface, store=False, prn=self.check_spoof)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface',
                        help='checks for specific interface')

    args = parser.parse_args()
    interface = args.interface

    # Create spoof detector obj and start process
    detector = SpoofDetector(interface)
    detector.start()
