__author__ = "Andrea Biancini, Jonas Geduldig"
__date__ = "January 3, 2014"
__license__ = "MIT"

import base64
from .constants import *
import requests


class BearerAuth(requests.auth.AuthBase):

    """Request bearer access token for oAuth2 authentication.

    :param consumer_key: Twitter application consumer key
    :param consumer_secret: Twitter application consumer secret
    :param proxies: Dictionary of proxy URLs (see documentation for python-requests).
    """

    def __init__(self, consumer_key, consumer_secret, proxies=None):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self.proxies = proxies
        self._bearer_token = self._get_access_token()

    def _get_access_token(self):
        token_url = '%s://%s.%s/%s' % (PROTOCOL,
                                       REST_SUBDOMAIN,
                                       DOMAIN,
                                       OAUTH2_TOKEN_ENDPOINT)
        auth = self._consumer_key + ':' + self._consumer_secret
        b64_bearer_token_creds = base64.b64encode(auth.encode('utf8'))
        params = {'grant_type': 'client_credentials'}
        headers = {}
        headers['User-Agent'] = USER_AGENT
        headers['Authorization'] = 'Basic ' + \
            b64_bearer_token_creds.decode('utf8')
        headers[
            'Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        try:
            response = requests.post(
                token_url,
                params=params,
                headers=headers,
                proxies=self.proxies)
            data = response.json()
            return data['access_token']
        except Exception as e:
            raise Exception(
                'Error while requesting bearer access token: %s' %
                e)

    def __call__(self, r):
        auth_list = [
            self._consumer_key,
            self._consumer_secret,
            self._bearer_token]
        if all(auth_list):
            r.headers['Authorization'] = "Bearer %s" % self._bearer_token
            return r
        else:
            raise Exception('Not enough keys passed to Bearer token manager.')
