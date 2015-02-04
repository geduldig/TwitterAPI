__title__ = 'TwitterAPI'
__version__ = '2.3.0-dev'
__author__ = 'Jonas Geduldig'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 Jonas Geduldig'


import logging


# No logging unless the client provides a handler
logging.getLogger(__name__).addHandler(logging.NullHandler())


try:
    from .TwitterOAuth import TwitterOAuth
    from .TwitterAPI import TwitterAPI, TwitterResponse, RestIterator, StreamingIterator
    from .TwitterRestPager import TwitterRestPager
except:
    pass


__all__ = [
    'TwitterAPI',
    'TwitterError',
    'TwitterOAuth',
    'TwitterRestPager'
]
