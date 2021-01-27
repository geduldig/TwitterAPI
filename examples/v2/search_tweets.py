from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError

QUERY = 'pizza'

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret, api_version='2')
	r = api.request('tweets/search/recent', {
		'query':QUERY, 
		'tweet.fields':'author_id',
		'expansions':'author_id'})

	for item in r:
		print(item)

	print('\nINCLUDES')
	print(r.json()['includes'])

	print('\nQUOTA')
	print(r.get_quota())

except TwitterRequestError as e:
	print(e.status_code)
	for msg in iter(e):
		print(msg)

except TwitterConnectionError as e:
	print(e)

except Exception as e:
	print(e)