# TwitterAPI #

This python package supports the latest Twitter API (version 1.1) with OAuth, and it works 
with the latest python versions in both 2.x and 3.x tracks.  

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

### Command-line Usage (cly.py) ###

For help:

	> python -m TwitterAPI.cli -h 

You will need to supply your Twitter application OAuth credentials.  The easiest option
is to enter them in TwitterAPI/credentials.txt.  The the default place where cli.py will
look for them.  You also can supply an alternative credentials file as a command-line
argument.

Call any REST API endpoint:

	> python -m TwitterAPI.cli -endpoint statuses/update -parameters status='my tweet'

Another example (here using abreviated option names) that parses selected output fields:

	> python -m TwitterAPI.cli -e search/tweets -p q=zzz count=10 -field screen_name text 

Calling any Streaming API endpoint works too:

	> python -m TwitterAPI.cli -e statuses/filter -p track=zzz -f screen_name text
	
If you do not include the -field (-f) option cly.py prints the entire JSON response object.  Or, to print just fields of interest add one or more field names after -field.

### Installation ###

	> pip install TwitterAPI
	
### Contributors ###

Jonas Geduldig
