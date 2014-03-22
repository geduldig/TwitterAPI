import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
from TwitterAPI import TwitterAPI


consumer_key = '<YOUR APPLICATION KEY>'
consumer_secret = '<YOUR APPLICATION SECRET>'


# obtain request token
oauth = OAuth1(consumer_key, consumer_secret)
r = requests.post(
    url='https://api.twitter.com/oauth/request_token',
    auth=oauth)
credentials = parse_qs(r.content)
request_key = credentials.get('oauth_token')[0]
request_secret = credentials.get('oauth_token_secret')[0]


# obtain authorization from resource owner
print(
    'Go here to authorize:\n  https://api.twitter.com/oauth/authorize?oauth_token=%s' %
    request_key)
verifier = raw_input('Enter your authorization code: ')


# obtain access token
oauth = OAuth1(
    consumer_key,
    consumer_secret,
    request_key,
    request_secret,
    verifier=verifier)
r = requests.post(url='https://api.twitter.com/oauth/access_token', auth=oauth)
credentials = parse_qs(r.content)
access_token_key = credentials.get('oauth_token')[0]
access_token_secret = credentials.get('oauth_token_secret')[0]


# access resource
api = TwitterAPI(
    consumer_key,
    consumer_secret,
    access_token_key,
    access_token_secret)
for item in api.request('statuses/filter', {'track': 'zzz'}):
    print(item['text'])
