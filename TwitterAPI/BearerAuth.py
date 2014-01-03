__author__ = "Andrea Biancini, Jonas Geduldig"
__date__ = "January 3, 2014"
__license__ = "MIT"

import base64
from .constants import USER_AGENT
import requests


class BearerAuth(requests.auth.AuthBase):
	"""Request bearer access token for oAuth2 authentication.
		
	:param token_url: Twitter oAuth2 token access URL
	:param consumer_key: Twitter application consumer key
	:param consumer_secret: Twitter application consumer secret
	"""
	
	def __init__(self, token_url, consumer_key, consumer_secret):
		self._token_url = token_url
		self._consumer_key = consumer_key
		self._consumer_secret = consumer_secret
		self._bearer_token = self._get_access_token()

	def _get_access_token(self):
		b64_bearer_token_creds = base64.b64encode(self._consumer_key + ':' + self._consumer_secret)
		params = {'grant_type':'client_credentials'}
		headers = {}
		headers['User-Agent'] = USER_AGENT
		headers['Authorization'] = 'Basic ' + b64_bearer_token_creds
		headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
		try:
			response = requests.post(self._token_url, params=params, headers=headers)
			data = response.json()
			return data['access_token']
		except Exception as e:
			raise Exception('Error while requesting bearer access token: %s' % e)

	def __call__(self, r):
		auth_list = [self._consumer_key, self._consumer_secret, self._bearer_token]
		if all(auth_list):
			r.headers['Authorization'] = "Bearer %s" % self._bearer_token
			return r
		else:
			raise Exception('Not enough keys passed to Bearer token manager.')
