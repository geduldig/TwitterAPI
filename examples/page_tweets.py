from TwitterAPI import TwitterAPI, TwitterRestPager


SEARCH_TERM = 'pizza'


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''


api = TwitterAPI(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET)

pager = TwitterRestPager(api, 'search/tweets', {'q': SEARCH_TERM})

for item in pager.get_iterator():
    print(item['text'] if 'text' in item else item)
