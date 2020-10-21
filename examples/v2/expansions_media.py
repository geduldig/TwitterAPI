from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError
import json

TWEET_ID = '1318585013944942593'
EXPANSIONS = 'attachments.media_keys'
MEDIA_FIELDS = 'duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics'

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret, api_version='2')
	r = api.request(f'tweets/:{TWEET_ID}', 
		{
			'expansions':EXPANSIONS, 
			'media.fields':MEDIA_FIELDS
		})

	for item in r:
		print(json.dumps(item, indent=2))

	print(r.get_quota())

except TwitterRequestError as e:
	print(e.status_code)
	for msg in iter(e):
		print(msg)

except TwitterConnectionError as e:
	print(e)

except Exception as e:
	print(e)