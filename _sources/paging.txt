Paging Results
==============

Paging refers to getting successive batches of results. The Streaming API endpoints in a sense do this inherently. REST API endpoints will never return more than a specificied maximum number of results. When you request `search/tweets`, for example, by default you will get at most 20 tweets. You can increase that number to a maximum of 100. This is the page size. Twitter provides a `way <http://dev.twitter.com/rest/public/timelines>`_ to get successive pages, so it is possible to get more than 100 tweets with `search/tweets`, just not in a single request.

If you don't want to implement paging yourself, you can use the `TwitterRestPager <./twitterrestpager.html>`_ helper class with any REST API endpoint that returns multiples of something. The following, for example, searches for all tweets containing 'pizza' that Twitter has stored -- about a week's worth.

.. code-block:: python 

    r = TwitterRestPager(api, 'search/tweets', {'q':'pizza', 'count':100})
    for item in r.get_iterator():
        if 'text' in item:
            print item['text']
        elif 'message' in item and item['code'] == 88:
            print 'SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message']
            break
