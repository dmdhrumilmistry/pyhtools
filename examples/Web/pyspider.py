from asyncio import run
from asyncio.exceptions import CancelledError
from argparse import ArgumentParser
from pyhtools.attackers.web.spider import Spider
from pyhtools.UI.colors import BRIGHT_RED


parser = ArgumentParser(prog='pyspider')
parser.add_argument('-t', '--target', dest='target_url', required=True,
                    help='url of the target eg: https://example.com')
args = parser.parse_args()

target_url = args.target_url
spider = Spider()
try:
    discovered_links = run(spider.start(
        target_url=target_url, print_links=True))
    print(f'[*] Total Links Found: {len(discovered_links)-1}')
except (EOFError, KeyboardInterrupt, CancelledError):
    print(BRIGHT_RED + "[!] Error: User Interrupted")
