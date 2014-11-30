__author__ = "Jonas Geduldig"
__date__ = "November 30, 2014"
__license__ = "MIT"


class TwitterError(Exception):
    """Base class for Twitter exceptions"""
    pass

class TwitterConnectionError(TwitterError):
    """Raised when the connection is broken"""
    pass
