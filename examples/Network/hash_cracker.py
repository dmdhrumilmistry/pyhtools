from argparse import ArgumentParser
from pyhtools.attackers.Network.pass_cracker import HashCracker
    
parser = ArgumentParser(prog='pass_cracker')
parser.add_argument('-m', '--mode', default='MD5', help='hash type to decrypt.')
parser.add_argument('-p', '--path', help='path to passwords file.')
parser.add_argument('-h', '--hash', help='hash value to decrypt.')

args = parser.parse_args()

pass_crack = HashCracker(args.m, args.p, args.h)
    