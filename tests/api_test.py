import sys
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager

# SAVE YOUR APPLICATION CREDENTIALS IN TwitterAPI/credentials.txt.

o = TwitterOAuth.read_file()
api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret)

"""
sys.stdout.write('%s\n' api.request('statuses/update', {'status':'This is another tweet!'}))
"""

api.request('search/tweets', {'q':'zzz'})
iter = api.get_iterator()
for item in iter:
	sys.stdout.write('%s\n' %item['text'])

"""
api.request('statuses/filter', {'locations':'-74,40,-73,41'})
iter = api.get_iterator()
for item in iter:
	sys.stdout.write('%s\n' %item['text'])

pager = TwitterRestPager(api, 'search/tweets', {'q':'love'});
iter = pager.get_iterator()
for item in iter:
	sys.stdout.write('%s\n' %item['text'])
"""
