|LOGO|
======

.. |LOGO| image:: https://raw.githubusercontent.com/geduldig/TwitterAPI/master/logo.png 
.. |BADGE_VERSION| image:: http://img.shields.io/pypi/v/TwitterAPI.svg
   :target: https://crate.io/packages/TwitterAPI 
.. |BADGE_CHAT| image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/geduldig/TwitterAPI
   :target: https://gitter.im/geduldig/TwitterAPI?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. |BADGE_2| image:: https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fv2
   :target: https://developer.twitter.com/en/docs/twitter-api 
.. |BADGE_LABS| image:: https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Flabs
   :target: https://developer.twitter.com/en/docs/labs 
.. |BADGE_ADS| image:: https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fadsv9
   :target: https://developer.twitter.com/en/docs/twitter-ads-api
.. |BADGE_1.1| image:: https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fstandard
   :target: https://developer.twitter.com/en/docs/twitter-api
.. |BADGE_PREMIUM| image:: https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fpremium
   :target: https://developer.twitter.com


TwitterAPI is a minimal python wrapper for the TwitterAPIs. A list of what it can do:

* Support for all V1.1 and V2 endpoints, plus Premium, Ads, Labs, Collections.
* OAuth1 and bearer token authentication, and proxy server authentication.
* Streaming endpoints.
* Paging results.
* The option to "hydrate" results returned by V2 endpoints. 
* Error handling.

Installation
------------

	> pip install TwitterAPI

Twitter API Version 1.1 Code Snippets 
-------------------------------------
[More examples in `TwitterAPI/examples/v1.1 <https://github.com/geduldig/TwitterAPI/tree/master/examples/v1.1>`_]

Search for recent tweets
::

	from TwitterAPI import TwitterAPI
	api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
	r = api.request('search/tweets', {'q':'pizza'})
	for item in r:
		print(item)

Stream tweets from New York City as they get tweeted
::

	r = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
	for item in r:
		print(item)

Twitter API Version 2 Code Snippets 
------------------------------------
[More examples in `TwitterAPI/examples/v2 <https://github.com/geduldig/TwitterAPI/tree/master/examples/v2>`_ ]

Search for recent tweets, and specify `fields` and `expansions`
::

	from TwitterAPI import TwitterAPI
	api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret, api_version='2')
	r = api.request('tweets/search/recent', {
		'query':'pizza', 
		'tweet.fields':'author_id',
		'expansions':'author_id'})
	for item in r:
		print(item)

One Method For Everything
-------------------------

The ``request()`` method works with all version 1.1 and version 2 endpoints. Typcally, ``request()`` takes two arguments: a Twitter endpoint and a dictionary of endpoint parameters.  

The method returns an object that will iterate either search results and streams. The returned object also gives you access to the raw response (``r.text``) and the HTTP status code (``r.status_code``). See the `requests <http://docs.python-requests.org/en/latest/user/quickstart/>`_ library documentation for more details.

Documentation
-------------
* `An Introduction <http://geduldig.github.io/TwitterAPI>`_
* `Authentication <http://geduldig.github.io/TwitterAPI/authentication.html>`_
* `Error Handling <http://geduldig.github.io/TwitterAPI/errors.html>`_
* `Paging Results <http://geduldig.github.io/TwitterAPI/paging.html>`_
* `Tiny Examples <http://geduldig.github.io/TwitterAPI/examples.html>`_
* `Fault Tolerant Streams and Pages <http://geduldig.github.io/TwitterAPI/faulttolerance.html>`_

Extra Goodies
-------------
Command-Line Utility (`examples/cli <https://github.com/geduldig/TwitterAPI/blob/master/examples/cli>`_)
