import re
import googlebooks
import requests
from bs4 import BeautifulSoup
from slackbot.bot import listen_to
from slackbot.bot import respond_to

COOKIES = {'lg_topic': 'libgen', }

HEADERS = {'Pragma': 'no-cache', 'DNT': '1', 'Accept-Language': 'en-US,en;q=0.8,it;q=0.6', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', }
VALID_URLS = ["libgen.pw/view", "libgen.io/ads", "bookfi.net/md5/", "b-ok.org/md5/"]
api = googlebooks.Api()


# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# requests.get('http://gen.lib.rus.ec/search.php?req=0321334876&open=0&res=25&view=simple&phrase=0&column=identifier', headers=headers, cookies=cookies)

def find_book(message, isbn):
	params = (('req', isbn), ('open', '0'), ('res', '25'), ('view', 'simple'), ('phrase', '0'), ('column', 'identifier'),)
	res = requests.get('http://gen.lib.rus.ec/search.php', headers=HEADERS, params=params, cookies=COOKIES)
	book = api.list('isbn:' + isbn)
	if book["totalItems"] != 0:
		message.reply("Searching for book " + json.dumps(book))
	page = BeautifulSoup(res.content, 'html.parser')
	valid = []
	for link in page.find_all('a', href=True):
		for URL in VALID_URLS:
			if link['href'] and URL in link['href']:
				valid.append(link['href'])
	if len(valid) is not 0:
		message.reply("I found a few links!")
		for i in range(0, 5):
			if len(valid) > i:
				message.reply(valid[i])
	else:
		message.reply("No links found")


@respond_to('ISBN (.*)', re.IGNORECASE)
def isbn(message, isbn):
	isbn = re.sub("[^0-9]", "", isbn)
	print(isbn)
	message.reply('Working on your request for ISBN {}'.format(isbn))
	find_book(message, isbn);


@listen_to('textbook ISBN (.*)', re.IGNORECASE)
def isbn(message, isbn):
	isbn = re.sub("[^0-9]", "", isbn)
	print(isbn)
	message.reply('Working on your request for ISBN {}'.format(isbn))
	find_book(message, isbn);
