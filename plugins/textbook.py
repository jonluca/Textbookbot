import re

import requests
from bs4 import BeautifulSoup
from slackbot.bot import listen_to
from slackbot.bot import respond_to

import plugins.googlebooks as googlebooks

COOKIES = {'lg_topic': 'libgen', }

HEADERS = {'Pragma': 'no-cache', 'DNT': '1', 'Accept-Language': 'en-US,en;q=0.8,it;q=0.6', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', }
VALID_URLS = ["libgen.pw/view", "libgen.io/ads", "bookfi.net/md5/", "b-ok.org/md5/"]
api = googlebooks.Api()


def find_book(message, isbn):
	# Params for the request
	params = (('req', isbn), ('open', '0'), ('res', '25'), ('view', 'simple'), ('phrase', '0'), ('column', 'identifier'),)
	res = requests.get('http://gen.lib.rus.ec/search.php', headers=HEADERS, params=params, cookies=COOKIES)
	# instantiate the google books api. Adds overhead but I like when it prints the title, so I'm keeping it
	book = api.list('isbn:' + isbn)
	if book["totalItems"] != 0:
		# I don't know how often this fails... Hopefully not too much haha
		message.reply("Searching for book " + book["items"][0]["volumeInfo"]["title"])

	# Parse HTMl
	page = BeautifulSoup(res.content, 'html.parser')
	valid = []

	# Definitely not optimal, but I gave myself 45 minutes to make this, so first thought that pops in my head is what I use haha
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


# Respond to DMs
@respond_to('ISBN (.*)', re.IGNORECASE)
def isbn(message, isbn):
	isbn = re.sub("[^0-9]", "", isbn)
	print(isbn)
	message.reply('Working on your request for ISBN {}'.format(isbn))
	find_book(message, isbn);


# Responds to mentions in channels its in
@listen_to('textbook ISBN (.*)', re.IGNORECASE)
def isbn(message, isbn):
	isbn = re.sub("[^0-9]", "", isbn)
	print(isbn)
	message.reply('Working on your request for ISBN {}'.format(isbn))
	find_book(message, isbn);
