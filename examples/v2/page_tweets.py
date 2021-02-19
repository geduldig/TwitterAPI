from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, TwitterPager

QUERY = 'pizza'

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret, api_version='2')
	pager = TwitterPager(api, 'tweets/search/recent', {'query':QUERY})
	
	for item in pager.get_iterator(new_tweets=False):
		print(item)

except TwitterRequestError as e:
	print(e.status_code)
	for msg in iter(e):
		print(msg)

except TwitterConnectionError as e:
	print(e)

except Exception as e:
	print(e)
