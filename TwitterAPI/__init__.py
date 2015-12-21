__title__ = 'TwitterAPI'
__version__ = '2.3.6'
__author__ = 'Jonas Geduldig'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 Jonas Geduldig'


import logging


# Suppress logging unless the client provides a handler
logging.getLogger(__name__).addHandler(logging.NullHandler())


try:
    from .TwitterAPI import TwitterAPI, TwitterResponse
    from .TwitterError import TwitterConnectionError, TwitterRequestError
    from .TwitterOAuth import TwitterOAuth
    from .TwitterRestPager import TwitterRestPager
except:
    pass


__all__ = [
    'TwitterAPI',
    'TwitterConnectionError',
    'TwitterRequestError',
    'TwitterOAuth',
    'TwitterRestPager'
]
