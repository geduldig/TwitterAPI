![](logo.png?raw=true)

TwitterAPI 
==========
[![Downloads](https://pypip.in/d/TwitterAPI/badge.png)](https://crate.io/packages/TwitterAPI)
[![Downloads](https://pypip.in/v/TwitterAPI/badge.png)](https://crate.io/packages/TwitterAPI) 

This Python package supports Twitter's REST and Streaming APIs (version 1.1) with OAuth 1.0 or OAuth 2.0.  It works with the latest Python versions in both 2.x and 3.x branches.  

Some Code Examples
------------------
*See TwitterAPI/cli.py and TwitterAPI/examples for more working examples.*

First, authenticate with your application credentials:

	from TwitterAPI import TwitterAPI
	api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

Tweet something:

	r = api.request('statuses/update', {'status':'This is a tweet!'})
	print r.status_code

Get some tweets:

	r = api.request('search/tweets', {'q':'pizza'})
	for item in r.get_iterator():
		print item

Stream tweets from New York City:

	r = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
	for item in r.get_iterator():
		print item
		
Notice that request() accepts both REST and Streaming API methods, and it takes two arguments: 1) the Twitter method, 2) a dictionary of method parameters.  In the above examples we use the get\_iterator() helper to get each tweet object.  This iterator knows how to iterate both REST and Streaming API results, in addition to error objects.  Alternatively, you have access to the response object returned by request().  From the response object you may call properties that return the raw response (r.text) and the http status code (r.status\_code).  See the documentation for the [Requests](http://docs.python-requests.org/en/latest/user/quickstart/) library for more info.

Command-Line Usage (cli.py)
---------------------------
For syntax help:

	> python -u -m TwitterAPI.cli -h 

You will need to supply your Twitter application OAuth credentials.  The easiest option is to save them in TwitterAPI/credentials.txt.  It is the default place where cli.py will look for them.  You also may supply an alternative credentials file as a command-line argument.

Call any REST API endpoint:

	> python -u -m TwitterAPI.cli -endpoint statuses/update -parameters status='my tweet'

Another example (here using abbreviated option names) that parses selected output fields:

	> python -u -m TwitterAPI.cli -e search/tweets -p q=zzz count=10 -field screen_name text 

Calling any Streaming API endpoint works too:

	> python -u -m TwitterAPI.cli -e statuses/filter -p track=zzz -f screen_name text

After the -field option you must supply one or more key names from the raw JSON response object.  This will print values only for these keys.  When the -field option is omitted cli.py prints the entire JSON response object.  

Installation
------------
	> pip install TwitterAPI

Documentation
-------------
* [Modules](http://geduldig.github.com/TwitterAPI)
	
Contributors
------------
* Jonas Geduldig
* Andrea Biancini
