from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError
import json

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')

	# GET STREAM RULES

	rule_ids = []
	r = api.request('tweets/search/stream/rules', method_override='GET')
	for item in r:
		if 'id' in item:
			rule_ids.append(item['id'])
		else:
			print(json.dumps(item, indent=2))

	# DELETE STREAM RULES

	if len(rule_ids) > 0:
		r = api.request('tweets/search/stream/rules', {'delete': {'ids':rule_ids}})
		print(f'[{r.status_code}] RULES DELETED: {json.dumps(r.json(), indent=2)}\n')

except TwitterRequestError as e:
	print(e.status_code)
	for msg in iter(e):
		print(msg)

except TwitterConnectionError as e:
	print(e)

except Exception as e:
	print(e)
