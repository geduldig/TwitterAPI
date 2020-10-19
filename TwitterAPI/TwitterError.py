__author__ = "geduldig"
__date__ = "November 30, 2014"
__license__ = "MIT"


import logging
import json


class TwitterError(Exception):

    """Base class for Twitter exceptions"""
    pass


class TwitterConnectionError(TwitterError):

    """Raised when the connection needs to be re-established"""

    def __init__(self, value):
        super().__init__(value)
        logging.warning('%s %s' % (type(value), value))


class TwitterRequestError(TwitterError):

    """Raised when request fails"""

    def __init__(self, status_code, msg=None):
        if msg is None:
            if status_code >= 500:
                msg = 'Twitter internal error (you may re-try)'
            else:
                msg = 'Twitter request failed'
        logging.info('Status code %d: %s' % (status_code, msg))
        super().__init__(msg)
        self.status_code = status_code
        self.msg = msg

    def __str__(self):
        return '%s (%d): %s' % (self.args, self.status_code, self.msg)


    def __iter__(self):
        try:
            msg = json.loads(self.msg)
            if 'errors' in msg:
                for error in msg['errors']:
                    yield error['message']
            elif 'detail' in msg:
                yield msg['detail']
            else:
                yield self.msg
        except:
            yield self.msg