# TwitterAPI #

### Scripting Usage ###

See TwitterAPI/cli.py for a working scripting example.  

First, authenticate with your application credentials:

	from TwitterAPI import TwitterAPI
	api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

Tweet something:

	api.request('statuses/update', {'status':'This is a tweet!'})

Get some tweets:

	api.request('search/tweets', {'q':'zzz'})
	iter = api.get_iterator()
	for item in iter:
		print item

Stream tweets from New York City:

	api.request('statuses/filter', {'locations':'-74,40,-73,41'})
	iter = api.get_iterator()
	for item in iter:
		print item

### Command-line Usage ###

For help:

	> python -m TwitterAPI.cli -h 

You will need to supply your Twitter application OAuth credentials.  The easiest option
is to enter them in TwitterAPI/credentials.txt.  The the default place where cli.py will
look for them.  You also can supply an alternative credentials file as a command-line
argument.

Call any REST API endpoint:

	> python -m TwitterAPI.cli -endpoint statuses/update -parameters status='my tweet'
	> python -m TwitterAPI.cli -e search/tweets -p q=zzz count=10 -field screen_name text 

Call any Streaming API endpoint (using the -field option to print only the screen_name and the tweet text):

	> python -m TwitterAPI.cli -e statuses/filter -p track=zzz -f screen_name text
	
If you do not include the -field (-f) option cly.py prints the entire JSON response object.
To print just fields of interest add one or more field names after -field.

### Installation ###

	> pip install TwitterAPI
	
### Contributors ###

Jonas Geduldig
