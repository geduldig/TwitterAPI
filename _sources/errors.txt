Error Handling
==============

Besides tweet statuses, the REST API and Streaming API iterators can return errors and other messages. It is up to the application to test what type of object has been returned. Message types are documented `here <http://dev.twitter.com/overview/api/response-codes>`_ and `here <http://dev.twitter.com/streaming/overview/messages-types>`_.

REST API Messages
-----------------

REST API endpoints can return many more types of messages than Streaming API endpoints. Depending on the endpoint, you may want to handle a particular type of message, such as exceeding a rate limit or posting a duplicate tweet. Here is a general pattern for simply printing out any message and error code:

.. code-block:: python

    r = api.request('search/tweets', {'q':'pizza'})
    for item in r.get_iterator():
        if 'text' in item:
            print item['text']
        elif 'message' in item:
            print '%s (%d)' % (item['message'], item['code'])

Streaming API Messages
----------------------

Streaming API endpoints return a variety of messages. Some are not errors. For example, a "limit" message contains the number of tweets missing from the stream. This happens when the number of tweets matching your filter exceeds a threshold set by Twitter. Other useful messages are "disconnect" and "delete".

.. code-block:: python

    r = api.request('statuses/filter', {'track':'pizza'})
    for item in r.get_iterator():
        if 'text' in item:
            print item['text']
        elif 'limit' in item:
            print '%d tweets missed' % item['limit']['track']
        elif 'disconnect' in item:
            print 'disconnecting because %s' % item['disconnect']['reason']
            break

Even if you are not interested in handling errors it is necessary to test that the object returned by an iterator is a valid tweet status before using the object. Valid tweet objects have a 'text' property (or a 'full_text' property if it is an extended tweet).