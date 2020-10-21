from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError
import json

TWEET_ID = '1275914014867050499'
EXPANSIONS = 'referenced_tweets.id'
TWEET_FIELDS = 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,text'

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret, api_version='2')
	r = api.request(f'tweets/:{TWEET_ID}', 
		{
			'expansions':EXPANSIONS, 
			'tweet.fields':TWEET_FIELDS
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