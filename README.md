# TwitterAPI #

_Easy access to all twitter.com endpoints_

More documentation coming shortly...

### Command-line Usage ###

For help:
	> python -m TwitterAPI.cli -h 

Call any REST API endpoint:
	> python -m TwitterAPI.cli -endpoint statuses/update -parameters status='my tweet'
	> python -m TwitterAPI.cli -e search/tweets -p q=zzz -field screen_name text 

Call any Streaming API endpoint:
	> python -m TwitterAPI.cli -e statuses/filter -p track=zzz -f text

### Scripting Usage ###

See TwitterAPI/cli.py for a working scripting example.  
	from TwitterAPI import TwitterAPI

	api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
	api.request('search/tweets', {'q':'zzz', 'count':10})
	iter = api.get_iterator()
	for item in iter:
		print item

### Installation ###

	> pip install TwitterAPI
	
### Contributors ###

Jonas Geduldig
