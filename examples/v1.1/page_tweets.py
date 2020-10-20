from TwitterAPI import TwitterAPI, TwitterPager

SEARCH_TERM = 'pizza'

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

pager = TwitterPager(api, 'search/tweets', {'q': SEARCH_TERM})

for item in pager.get_iterator():
    print(item['text'] if 'text' in item else item)