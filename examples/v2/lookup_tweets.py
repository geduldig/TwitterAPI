from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError

TWEET_IDS = ['964575983633252353', '1497014169178185730']

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret, api_version='2')
	r = api.request(f'tweets',{'ids':",".join(TWEET_IDS)})

	for item in r:
		print(item)

	print(r.get_quota())

except TwitterRequestError as e:
	print(e.status_code)
	for msg in iter(e):
		print(msg)

except TwitterConnectionError as e:
	print(e)

except Exception as e:
	print(e)