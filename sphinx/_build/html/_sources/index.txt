.. TwitterAPI documentation master file, created by
   sphinx-quickstart on Sat Sep 27 12:02:24 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

*Minimal Python wrapper for Twitter's REST and Streaming APIs*

The principle behind TwitterAPI's design is to provide a single method for accessing any Twitter API endpoint. The method may be called with *any* endpoint found on Twitter's `developer site <https://dev.twitter.com/overview/documentation>`_, the complete reference for all endpoint. The benefits of a single method approach is very little code and just a single method to learn. Here is a quck example:

.. code-block:: python

    from TwitterAPI import TwitterAPI
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    r = api.request('search/tweets', {'q':'pizza'})
    print r.status_code

If you want the response string containing the raw tweets you would use ``r.text``. However, you also have the option of a powerful iterator:

.. code-block:: python

    for item in r.get_iterator():
        print item['user']['screen_name'], item['text']

As you can see, the iterator returns decoded JSON objects. What makes the iterator very powerful is it works with both REST API and Streaming API endpoints. No syntax changes required; just supply the endpoint and the parameters.

TwiterAPI works with Python 2 and Python 3. It authenticates using either OAauth 1 or OAuth 2. Proxy authentication is also supported. All with very little code change for you.

Modules
=======

.. toctree::
   :maxdepth: 2

   twitterapi.rst

Optional:

.. toctree::
   :maxdepth: 2

   twitterrestpager.rst
   twitteroauth.rst
