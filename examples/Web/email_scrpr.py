from argparse import ArgumentParser
from pyhtools.attackers.web.email_scraper import EmailScraper
from pyhtools.UI.colors import BRIGHT_RED

parser = ArgumentParser(prog='email_scraper')
parser.add_argument('-u', '--url', help='url to base email search on.')
parser.add_argument('-c', '--count', default=100, help='number of emails to scrape.', type=int)
    
args = parser.parse.args()

email_scrpr = EmailScraper(args.u, args.c)