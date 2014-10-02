Tiny Examples
=============

All the examples assume `api` is an authenticated instance of `TwitterAPI <./twitterapi.html>`_. Typically, this is done as follows:

.. code-block:: python

    api = TwitterAPI(consumer_key, 
                     consumer_secret, 
                     access_token_key, 
                     access_token_secret)


Get your last 50 tweets
-----------------------

.. code-block:: python 

    r = api.request('statuses/home_timeline', {'count':50})
    for item in r.get_iterator():
        if 'text' in item:
            print item['text']

Get your entire timeline
------------------------

.. code-block:: python 

    pager = TwitterRestPager(api, 'statuses/home_timeline', {'count':200})
    for item in pager.get_iterator(wait=60):
        if 'text' in item:
            print item['text']

Post a tweet
------------

.. code-block:: python 

    r = api.request('statuses/update', {'status': 'I need pizza!'})
    print 'SUCCESS' if r.status_code == 200 else 'FAILURE'

Post a tweet with a picture
---------------------------

.. code-block:: python 

    file = open('./image_of_pizza.png', 'rb')
    data = file.read()
    r = api.request('statuses/update_with_media',
                    {'status':'I found pizza!'},
                    {'media[]':data})
    print 'SUCCESS' if r.status_code == 200 else 'FAILURE'

Stream tweets 
-------------

.. code-block:: python 

    r = api.request('statuses/filter', {'track':'pizza'})
    for item in r.get_iterator():
        if 'text' in item:
            print item['text']
