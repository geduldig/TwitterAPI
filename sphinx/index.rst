Introduction
============

*Minimal Python wrapper for Twitter's REST and Streaming APIs*

The principle behind TwitterAPI's design is to provide a single method for accessing the Twitter API. You can call the ``request`` method with *any* endpoint found on Twitter's `developer site <https://dev.twitter.com/overview/documentation>`_, the complete reference for all endpoints. The benefits of a single-method approach are: less code for me to maintain, and just a single method for you to learn. Here is a quck example:

.. code-block:: python

    from TwitterAPI import TwitterAPI
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    r = api.request('search/tweets', {'q':'pizza'})
    print r.status_code

If you want Twitter's entire response as one long string, containing tweets in this example, you would use ``r.text``. But, often an iterator is more useful:

.. code-block:: python

    for item in r.get_iterator():
        print item['user']['screen_name'], item['text']

The iterator returns decoded JSON objects. What makes the iterator very powerful is it works with both REST API and Streaming API endpoints. No syntax changes required; just supply any endpoint and parameters that are found on Twitter's dev site.

TwitterAPI is compatible with Python 2 and Python 3. It authenticates using either OAauth 1 or OAuth 2. It also supports web proxy server authentication. All with very little code change for you.

Topics
======

.. toctree::
   :maxdepth: 1

   authentication.rst
   errors.rst
   paging.rst
   examples.rst
   faulttolerance.rst

Modules
=======

.. toctree::
   :maxdepth: 2

   twitterapi.rst
   twittererror.rst

Optional:

.. toctree::
   :maxdepth: 2

   twitterrestpager.rst
   twitteroauth.rst
