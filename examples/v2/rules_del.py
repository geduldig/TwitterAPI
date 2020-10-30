from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError
import json

RULE_IDS = [
	"1317935598431309824",
	"1321813278532751361",
]

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')

	# DELETE STREAM RULES

	r = api.request('tweets/search/stream/rules', {'delete': {'ids':RULE_IDS}})
	print(f'[{r.status_code}] RULES DELETED: {json.dumps(r.json(), indent=2)}\n')

except TwitterRequestError as e:
	print(e.status_code)
	for msg in iter(e):
		print(msg)

except TwitterConnectionError as e:
	print(e)

except Exception as e:
	print(e)
