from argparse import ArgumentParser
from pyhtools.attackers.Network.ssid_connector import Connector

parser = ArgumentParser(prog='ssid_connector')
parser.add_argument('-p', '--path', help='path to directory containing passwords file.')
args = parser.parse_args()

args = parser.parse_args()

connector = Connector(args.p)