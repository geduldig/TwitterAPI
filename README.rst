|LOGO|
==============================================
|BADGE_DOWNLOADS| |BADGE_VERSION| |BADGE_CHAT|
==============================================

.. |LOGO| image:: https://raw.githubusercontent.com/geduldig/TwitterAPI/master/logo.png 
.. |BADGE_DOWNLOADS| image:: https://img.shields.io/pypi/dm/TwitterAPI.svg
   :target: https://crate.io/packages/TwitterAPI 
.. |BADGE_VERSION| image:: http://img.shields.io/pypi/v/TwitterAPI.svg
   :target: https://crate.io/packages/TwitterAPI 
.. |BADGE_CHAT| image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/geduldig/TwitterAPI
   :target: https://gitter.im/geduldig/TwitterAPI?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

TwitterAPI is a Python package for accessing Twitter's REST API and Streaming API. It supports OAuth 1.0 and OAuth 2.0 authentication.  And, it works with the latest Python versions in both 2.x and 3.x branches. 

Installation
------------
From the command line::

	pip install TwitterAPI

Documentation
-------------
* `An Introduction <http://geduldig.github.com/TwitterAPI>`_
* `Authentication <http://geduldig.github.com/TwitterAPI/authentication.html>`_
* `Error Handling <http://geduldig.github.com/TwitterAPI/errors.html>`_
* `Paging Results <http://geduldig.github.com/TwitterAPI/paging.html>`_
* `Tiny Examples <http://geduldig.github.com/TwitterAPI/examples.html>`_
* `Fault Tolerant Streams and Pages <http://geduldig.github.com/TwitterAPI/faulttolerance.html>`_

Some Code...
------------
[See `TwitterAPI/examples <https://github.com/geduldig/TwitterAPI/tree/master/examples>`_ for working examples.]

First, authenticate with your application credentials::

	from TwitterAPI import TwitterAPI
	api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

Tweet something::

	r = api.request('statuses/update', {'status':'This is a tweet!'})
	print(r.status_code)

Get tweet by its id::

	r = api.request('statuses/show/:%d' % 210462857140252672)
	print(r.text)

Get some tweets::

	r = api.request('search/tweets', {'q':'pizza'})
	for item in r:
		print(item)

Stream tweets from New York City::

	r = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
	for item in r:
		print(item)
		
Notice that ``request()`` works with both REST and Streaming API endpoints. Usually ``request()`` takes two arguments: a Twitter endpoint and a dictionary of endpoint parameters.  The above examples use ``get_iterator()`` to consume each tweet object.  The iterator knows how to iterate both REST and Streaming API results.  

You also have access to the response object returned by ``request()``.  From a response object ``r`` you can get the raw response with ``r.text`` and the HTTP status code with ``r.status_code``.  See the `requests <http://docs.python-requests.org/en/latest/user/quickstart/>`_ library documentation for more details.

Command-Line Utility (`examples/cli.py <https://github.com/geduldig/TwitterAPI/blob/master/examples/cli.py>`_)
--------------------------------------------------------------------------------------------------------------
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
