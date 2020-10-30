from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError
import json

QUERY = 'pizza"'

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')

	# ADD STREAM RULES

	r = api.request('tweets/search/stream/rules', {'add': [{'value':QUERY}]})
	print(f'[{r.status_code}] RULE ADDED: {json.dumps(r.json(), indent=2)}\n')

except TwitterRequestError as e:
	print(e.status_code)
	for msg in iter(e):
		print(msg)

except TwitterConnectionError as e:
	print(e)

except Exception as e:
	print(e)
