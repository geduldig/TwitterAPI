# Print a user's timeline. This will get up to 3,200 tweets, which
# is the maximum the Twitter API allows.

from TwitterAPI import TwitterAPI, TwitterPager

SCREEN_NAME = 'TheTweetOfGod'

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 auth_type='oAuth2')

pager = TwitterPager(api, 
                     'statuses/user_timeline', 
                     {'screen_name':SCREEN_NAME, 'count':200})

count = 0
for item in pager.get_iterator(wait=3.5):
	if 'text' in item:
		count = count + 1
		print(count, item['text'])
	elif 'message' in item:
		print(item['message'])
		break