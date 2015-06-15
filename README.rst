===================================================
|LOGO| TwitterAPI |BADGE_DOWNLOADS| |BADGE_VERSION|
===================================================

.. |LOGO| image:: https://raw.githubusercontent.com/geduldig/TwitterAPI/master/logo.png 
   :height: 50
.. |BADGE_DOWNLOADS| image:: https://img.shields.io/pypi/dm/TwitterAPI.svg
   :target: https://crate.io/packages/TwitterAPI 
.. |BADGE_VERSION| image:: http://img.shields.io/pypi/v/TwitterAPI.svg
   :target: https://crate.io/packages/TwitterAPI 

This Python package supports Twitter's REST and Streaming APIs (version 1.1) with OAuth 1.0 or OAuth 2.0.  It works with the latest Python versions in both 2.x and 3.x branches.  

Some Code Examples
------------------
[See `TwitterAPI/examples <https://github.com/geduldig/TwitterAPI/tree/master/examples>`_ for working examples.]

First, authenticate with your application credentials::

	from TwitterAPI import TwitterAPI
	api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

Tweet something::

	r = api.request('statuses/update', {'status':'This is a tweet!'})
	print r.status_code

Get some tweets::

	r = api.request('search/tweets', {'q':'pizza'})
	for item in r:
		print item

Stream tweets from New York City::

	r = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
	for item in r:
		print item
		
Notice that ``request()`` accepts both REST and Streaming API methods, and it takes two arguments: the Twitter method, and a dictionary of method parameters.  In the above examples we use ``get_iterator()`` to get each tweet object.  The iterator knows how to iterate both REST and Streaming API results.  Alternatively, you have access to the response object returned by ``request()``.  From the response object ``r`` you can get the raw response with ``r.text`` or the HTTP status code with ``r.status_code``.  See the `requests <http://docs.python-requests.org/en/latest/user/quickstart/>`_ library documentation for more details.

Command-Line Usage (examples/cli.py)
---------------------------
For syntax help::

	python cli.py -h 

You will need to supply your Twitter application OAuth credentials.  The easiest option is to save them in TwitterAPI/credentials.txt.  It is the default place where cli.py will look for them.  You also may supply an alternative credentials file as a command-line argument.

Call any REST API endpoint::

	python cli.py -endpoint statuses/update -parameters status='my tweet'

Another example (here using abbreviated option names) that parses selected output fields::

	python cli.py -e search/tweets -p q=zzz count=10 -field screen_name text 

Calling any Streaming API endpoint works too::

	python cli.py -e statuses/filter -p track=zzz -f screen_name text

After the ``-field`` option you must supply one or more key names from the raw JSON response object.  This will print values only for these keys.  When the ``-field`` option is omitted cli.py prints the entire JSON response object.  

Installation
------------
From the command line::

	pip install TwitterAPI

Documentation
-------------
* `An introduction <http://geduldig.github.com/TwitterAPI>`_
