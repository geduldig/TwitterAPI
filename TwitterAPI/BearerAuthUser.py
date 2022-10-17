__author__ = "Andrea Biancini, geduldig"
__date__ = "January 3, 2014"
__license__ = "MIT"


from .constants import *
import requests


class BearerAuthUser(requests.auth.AuthBase):

    """Request bearer access token for oAuth2 authentication.

    :param consumer_key: Twitter application consumer key
    :param consumer_secret: Twitter application consumer secret
    :param proxies: Dictionary of proxy URLs (see documentation for python-requests).
    """

    def __init__(self, oauth2_access_token, proxies=None, user_agent=None):
        self.proxies = proxies
        self.user_agent = user_agent
        self._bearer_token = oauth2_access_token


    def __call__(self, r):
        auth_list = [
            self._bearer_token]
        if all(auth_list):
            r.headers['Authorization'] = "Bearer %s" % self._bearer_token
            return r
        else:
            raise Exception('Not enough keys passed to Bearer token manager.')
