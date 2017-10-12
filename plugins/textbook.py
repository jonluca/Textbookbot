import re
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import requests
from bs4 import BeautifulSoup

cookies = {
    'lg_topic': 'libgen',
}

headers = {
    'Pragma': 'no-cache',
    'DNT': '1',
    'Accept-Language': 'en-US,en;q=0.8,it;q=0.6',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
}


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# requests.get('http://gen.lib.rus.ec/search.php?req=0321334876&open=0&res=25&view=simple&phrase=0&column=identifier', headers=headers, cookies=cookies)

def find_book(isbn):
	params = (('req', isbn), ('open', '0'), ('res', '25'), ('view', 'simple'), ('phrase', '0'), ('column', 'identifier'),)
	res = requests.get('http://gen.lib.rus.ec/search.php', headers=headers, params=params, cookies=cookies)
	print(res);

@respond_to('ISBN (.*)', re.IGNORECASE)
def isbn(message, isbn):
    message.reply('Working on your request for ISBN {}'.format(isbn))
    find_book(isbn);