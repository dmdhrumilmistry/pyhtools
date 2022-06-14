from argparse import ArgumentParser
from pyhtools.detectors.arp_spoof_detector import SpoofDetector

parser = ArgumentParser()
parser.add_argument('-i', '--interface', dest='interface',
                    help='checks for specific interface')

args = parser.parse_args()
interface = args.interface

# Create spoof detector obj
detector = SpoofDetector(interface)
detector.capture_packets()
