Paging Results
==============

Whether one is searching for tweets with `search/tweets` or downloading a user's timeline with `statuses/user_timeline` Twitter limits the number of tweets. So, in order to get more tweets, one must make successive requests and with each request skip the previously acquired tweets. This is done by specifying the tweet id from where to start. Twitter has a description `here <http://dev.twitter.com/rest/public/timelines>`_. If you don't want to implement paging yourself, you can use the `TwitterPager <./twitterpager.html>`_ helper class with any REST API endpoint that returns multiples of something. The following, for example, searches for all tweets containing 'pizza' that Twitter has stored -- up to about a week's worth maximum.

.. code-block:: python 

    r = TwitterPager(api, 'search/tweets', {'q':'pizza', 'count':100})
    for item in r.get_iterator():
        if 'text' in item:
            print item['text']
        elif 'message' in item and item['code'] == 88:
            print 'SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message']
            break

By default there is a built-in wait time of 5 seconds between successive calls. This value is overridden with an argument to `get_iterator()`. See the documentation also to learn how to wait for new tweets. In other words, the iterator can be setup to poll for newer pages of tweets rather than older pages.