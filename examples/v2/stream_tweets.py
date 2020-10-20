from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError

QUERY = 'pizza'

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')

	# ADD STREAM RULES

	r = api.request('tweets/search/stream/rules', {'add': [{'value':QUERY}]})
	print(f'[{r.status_code}] RULE ADDED: {r.text}')
	if r.status_code != 201: exit()

	# GET STREAM RULES

	r = api.request('tweets/search/stream/rules', method_override='GET')
	print(f'[{r.status_code}] RULES: {r.text}')
	if r.status_code != 200: exit()

	# START STREAM

	r = api.request('tweets/search/stream')
	print(f'[{r.status_code}] START...')
	if r.status_code != 200: exit()
	for item in r:
		print(item)

except TwitterRequestError as e:
	print(e.status_code)
	for msg in iter(e):
		print(msg)

except TwitterConnectionError as e:
	print(e)

except Exception as e:
	print(e)