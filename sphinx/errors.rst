Error Handling
==============

In addition to returning tweet statuses, the iterators for REST API and Streaming API endpoints return error and other messages. It is up to the application to test what type of object has been returned. The documentation is `here <http://dev.twitter.com/overview/api/response-codes>`_ and `here <http://dev.twitter.com/streaming/overview/messages-types>`_.

REST API Messages
-----------------

REST API endpoints can return many more types of messages than Streaming API endpoints. Depending on the endpoint, you may want to handle a particular type of message, such as exceeding a rate limit or posting a duplicate tweet. Testing the error code returned with the message makes this easy. Here is a general pattern for simply printing out any message and error code:

.. code-block:: python

    r = api.request('search/tweets', {'q':'pizza'})
    for item in r.get_iterator():
        if 'text' in item:
            print item['text']
        elif 'message' in item:
            print '%s (%d)' % (item['message'], item['code'])

Streaming API Messages
----------------------

Streaming API endpoints return a variety of messages, none are really errors. For example, a 'limit' message contains the number of tweets missing from the stream. This happens when you filter for tweets containing a common word. Other useful messages are 'disconnect' and 'delete'. The pattern is similar to the one preceding:

.. code-block:: python

    r = api.request('statuses/filter', {'track':'pizza'})
    for item in r.get_iterator():
        if 'text' in item:
            print item['text']
        elif 'limit' in item:
            print '%d tweets missed' % item['limit'].get('track')
        elif 'disconnect' in item:
            print 'disconnecting because %s' % item['disconnect'].get('reason')
            break

Even if you are not interested in handling errors it is necessary to test that the object returned by an iterator is a valid tweet status before using the object.