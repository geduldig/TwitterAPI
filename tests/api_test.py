import codecs
import sys
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager

try:
	# python 3
	sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
	sys.stderr = codecs.getwriter('utf8')(sys.stderr.buffer)
except:
	# python 2
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	sys.stderr = codecs.getwriter('utf8')(sys.stderr)


# SAVE YOUR APPLICATION CREDENTIALS IN TwitterAPI/credentials.txt.
o = TwitterOAuth.read_file()
api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret)


# GET 20 TWEETS CONTAINING 'ZZZ'
api.request('search/tweets', {'q':'zzz'})
iter = api.get_iterator()
for item in iter:
	sys.stdout.write('%s\n' % item['text'])

"""
# POST A TWEET 
sys.stdout.write('%s\n' % api.request('statuses/update', {'status':'This is another tweet!'}))

# STREAM TWEETS FROM AROUND NYC
api.request('statuses/filter', {'locations':'-74,40,-73,41'})
iter = api.get_iterator()
for item in iter:
	sys.stdout.write('%s\n' % item['text'])

# GET TWEETS FROM THE PAST WEEK OR SO CONTAINING 'LOVE'
pager = TwitterRestPager(api, 'search/tweets', {'q':'love'});
iter = pager.get_iterator()
for item in iter:
	sys.stdout.write('%s\n' % item['text'])
"""