__author__ = "Jonas Geduldig"
__date__ = "November 30, 2014"
__license__ = "MIT"


import logging


class TwitterError(Exception):

    """Base class for Twitter exceptions"""
    pass


class TwitterConnectionError(TwitterError):

    """Raised when the connection needs to be re-established"""

    def __init__(self, value):
        super(Exception, self).__init__(value)
        logging.warning('%s %s' % (type(value), value))
