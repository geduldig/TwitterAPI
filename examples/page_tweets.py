from TwitterAPI import TwitterAPI, TwitterRestPager

SEARCH_TERM = 'pizza'

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

pager = TwitterRestPager(api, 'search/tweets', {'q': SEARCH_TERM})

for item in pager.get_iterator():
    print(item['text'] if 'text' in item else item)