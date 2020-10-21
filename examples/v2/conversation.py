from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, TwitterPager
import json

CONVERSION_ID = '1318769013640450048'

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')
	pager = TwitterPager(api, 'tweets/search/recent', 
		{
			'query':f'conversation_id:{CONVERSION_ID}',
			'tweet.fields':'conversation_id'
		})

	# wait=2 means wait 2 seconds between each request.
	# The rate limit is 450 request per 15 minutes, or
	# 15*60/450 = 2 seconds
	for item in pager.get_iterator(wait=2):
		print(json.dumps(item, indent=2))

except TwitterRequestError as e:
	print(e.status_code)
	for msg in iter(e):
		print(msg)

except TwitterConnectionError as e:
	print(e)

except Exception as e:
	print(e)