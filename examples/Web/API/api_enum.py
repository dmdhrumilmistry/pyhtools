from ast import literal_eval
from asyncio import run
from argparse import ArgumentParser
from pyhtools.attackers.web.api.discover import APIdiscover
from sys import exit


parser = ArgumentParser(prog='api_enum')
parser.add_argument('-u', '--url', dest='url', required=True,
                    help='base url of web application API')
parser.add_argument('-w', '--wordlist', dest='wordlist_path',
                    required=True, help='endpoints wordlist file path')
parser.add_argument('-rl', '--rate-limit', dest='rate_limit', type=int,
                    default=20, help='number of requests to send concurrently during enumeration')
parser.add_argument('-d', '--delay', dest='delay', type=float,
                    default=0.05, help='delay between requests in seconds')
parser.add_argument('-H', '--header', dest='headers', default="{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}",
                    type=str, help='pass header argument in request. `Note:` supplied headers won\'t be passed during redirection (http->https)')
parser.add_argument('-mc', '--match-codes', dest='match_codes',
                    nargs='+', type=int, default=[200, 301, 401, 403, 405], help='display or save api endpoints only matching provided http response status codes')
parser.add_argument('-o', '--output-file', dest='output_file_path', type=str,
                    help='saves results in json format to provided output file path', required=False, default=None)

args = parser.parse_args()

# convert header str to dict
try:
    headers = literal_eval(args.headers)
except SyntaxError:
    print(
        '[Error] use header switch as followed: -H \'{"Authorization":"Bearer <token>"}\'')
    exit()

discoverer = APIdiscover(
    base_url=args.url,
    match_codes=args.match_codes,
    rate_limit=args.rate_limit,
    delay=args.delay,
    output_file_path=args.output_file_path,
    headers=headers,
)

run(
    discoverer.start_enum_from_file(wordlist_file=args.wordlist_path)
)
