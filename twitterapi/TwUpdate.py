__author__ = "Jonas Geduldig"
__date__ = "December 3, 2012"
__license__ = "MIT"

import json
import oauth2 as oauth
import urllib

API_ENDPOINT_URL = 'https://api.twitter.com/1.1/statuses/update.json'

class TwUpdate:
	"""Accesses Twitter's REST API for posting tweets"""

	def __init__(self, oauth_credentials):
		"""Configure the streaming request

		Parameters
		----------
		oauth_credentials : TwCredentials
			The consumer and access token keys and secrets.

		"""
		self.oauth_credentials = oauth_credentials
		self.client = None
		self._setup_request()

	def _setup_request(self):
		oauth_token = oauth.Token(key=self.oauth_credentials.access_token_key, secret=self.oauth_credentials.access_token_secret)
		oauth_consumer = oauth.Consumer(key=self.oauth_credentials.consumer_key, secret=self.oauth_credentials.consumer_secret)
		self.client = oauth.Client(oauth_consumer, oauth_token)

	def post(self, parameters):
		"""Upload a tweet

		Parameters
		----------
		parameters: dict
			Names and values for the statuses/update URL endpoint.
			See https://dev.twitter.com/docs/api/1.1/post/statuses/update.

		Raises
		------
		HTTP errors.

		"""
		parameters = urllib.urlencode(parameters)
		try:
			headers, content = self.client.request(API_ENDPOINT_URL, 'POST', parameters)
			content = json.loads(content)
			if headers.status != 200:
				if 'errors' in content:
					raise Exception('Error: %s' % content['errors'][0].get('message'))
				else:
					raise Exception('HTTP error: %s' & headers.status)
		except IOError, e:
			if hasattr(e, 'reason'):
				raise Exception('Server unreachable: %s' % e.reason)
			elif hasattr(e, 'code'):
				raise Exception('Server cannot fulfill the request: %s' % e.code)
