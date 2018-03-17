Fault Tolerant Streams and Pages
================================

There are a number of reasons for a stream to stop. Twitter will break your connection if you have more than two streams open with the same credentials, or if your credentials are not valid. Occassionally, the problem will be internal to Twitter and you will be disconnected. Other causes might be network instability or connection timeout.

Endless Stream
--------------

In order to keep a Streaming API request going indefinitely, you will need to re-make the request whenever the connection drops. TwitterAPI defines two exception classes for this purpose. 

`TwitterRequestError <./twittererror.html>`_ is thrown whenever the request fails (i.e. when the response status code is not 200). A status code of 500 or higher indicates a server error which is safe to ignore. Any other status code indicates an error with your request which you should fix before re-trying.

`TwitterConnectionError <./twittererror.html>`_ is thrown when the connection times out or is interrupted. You can always immediately try making the request again.

Sometimes Twitter will inform you to close the connection by sending you a "disconnect" message. The message will contain a code which indicates the reason. Messages with a code of 2, 5, 6, or 7 are serious and you will need to fix the problem before making a new request. You can ignore all other messages.

.. code-block:: python

    while True:
        try:
            iterator = api.request('statuses/filter', {'track':'pizza'}).get_iterator()
            for item in iterator:
                if 'text' in item:
                    print(item['text'])
                elif 'disconnect' in item:
                    event = item['disconnect']
                    if event['code'] in [2,5,6,7]:
                        # something needs to be fixed before re-connecting
                        raise Exception(event['reason'])
                    else:
                        # temporary interruption, re-try request
                        break
        except TwitterRequestError as e:
            if e.status_code < 500:
                # something needs to be fixed before re-connecting
                raise
            else:
                # temporary interruption, re-try request
                pass
        except TwitterConnectionError:
            # temporary interruption, re-try request
            pass

Last Week's Pages
-----------------

Requests for REST API endpoints can throw `TwitterRequestError <./twittererror.html>`_ and `TwitterConnectionError <./twittererror.html>`_. They do not, however, return "disconnect" messages. Twitter returns error messages for these endpoints with "message". Most of these errors require attention before re-trying the request, except those with codes of 130 or 131, which are internal server errors.

For making continuos REST API requests (i.e. paging), TwitterAPI provides `TwitterPager <./paging.html>`_. If you use this class to request tweets that have been posted back to one week old, for example, the class's iterator will handle both types of exceptions automatically. The iterator also handles "message" objects with 130 or 131 codes for you. Any other "message" object gets passed on for you to handle.

One final consideration is the endpoint's rate limit, determinted by the endpoint and whether you authenticate with oAuth 1 or oAuth 2. By default, the iterator waits 5 seconds between requests. This is sufficient for 180 requests in 15 minutes, the rate limit for "search/tweets" with oAuth 1. You can do better with oAuth 2. It permits 450 requests every 15 minutes, or 1 request per 2 seconds. The example below sets the wait assuming oAuth 2 rate limits.

.. code-block:: python

    iterator = TwitterPager(api, 'search/tweets', {'q':'pizza'}).get_iterator(wait=2)
    for item in iterator:
        if 'text' in item:
            print(item['text'])
        elif 'message' in item:
            # something needs to be fixed before re-connecting
            raise Exception(item['message'])