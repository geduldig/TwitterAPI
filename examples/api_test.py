import codecs
from datetime import datetime
import sys
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager


try:
    # python 3
    sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
except:
    # python 2
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)


# SAVE YOUR APPLICATION CREDENTIALS IN TwitterAPI/credentials.txt.
o = TwitterOAuth.read_file()

# Using OAuth1...
api = TwitterAPI(
    o.consumer_key,
    o.consumer_secret,
    o.access_token_key,
    o.access_token_secret)

# Using OAuth2...
#api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type="oAuth2")


TEST_NUMBER = 0


try:
    if TEST_NUMBER == 0:

        # VERIFY YOUR CREDS
        r = api.request('account/verify_credentials')
        print(r.text)

    if TEST_NUMBER == 1:

        # POST A TWEET
        r = api.request('statuses/update',
                        {'status': 'the time is now %s' % datetime.now()})
        print(r.status_code)

    if TEST_NUMBER == 2:

        # GET 5 TWEETS CONTAINING 'ZZZ'
        for item in api.request('search/tweets', {'q': 'zzz', 'count': 5}):
            print(item['text'] if 'text' in item else item)

    if TEST_NUMBER == 3:

        # STREAM TWEETS FROM AROUND NYC
        for item in api.request('statuses/filter', {'locations': '-74,40,-73,41'}):
            print(item['text'] if 'text' in item else item)

    if TEST_NUMBER == 4:

        # GET TWEETS FROM THE PAST WEEK OR SO CONTAINING 'LOVE'
        pager = TwitterRestPager(api, 'search/tweets', {'q': 'love'})
        for item in pager.get_iterator():
            print(item['text'] if 'text' in item else item)

except Exception as e:
    print(e)
