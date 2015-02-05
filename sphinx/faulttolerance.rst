Fault Tolerant Streams and Pages
================================

111

Endless Stream
--------------

AAA

.. code-block:: python

    while True:
        try:
            iterator = api.request('statuses/filter', {'track':'pizza').get_iterator()
            for item in iterator:
                if 'text' in item:
                    print(item['text'])
                elif 'disconnect' in item:
                    event = item['disconnect']
                    if event['code'] in [2,5,6,7]:
                        raise Exception(event['reason'])
                    break
        except TwitterRequestError as e:
            if e.status_code < 500:
                raise
        except TwitterConnectionError:
            pass

Last Week's Pages
-----------------

BBB

.. code-block:: python

    iterator = TwitterRestPager(api, 'search/tweets', {'q':'pizza').get_iterator(wait=5.1)
    try:
        for item in iterator:
            if 'text' in item:
                print(item['text'])
            elif 'message' in item:
                raise Exception(item['message'])

CCC
