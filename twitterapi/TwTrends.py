__author__ = "Jonas Geduldig"
__date__ = "December 8, 2012"
__license__ = "MIT"

from datetime import datetime
import json
import oauth2 as oauth
import time
import urllib

API_ENDPOINT_URL_PLACE = 'https://api.twitter.com/1.1/trends/place.json'
API_ENDPOINT_URL_AVAILABLE = 'https://api.twitter.com/1.1/trends/available.json'

class TwTrends:
	"""Accesses Twitter's REST API for getting trends"""

	def __init__(self, oauth_credentials):
		"""Configure the search request

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
		
	def worldwide(self, exclude_hashtags=False):
		"""Generator of worldwide trends (most frequently tweeted words and hashtags)
		
		Parameters
		----------
		exclude_hashtags : boolean (default False)
			When false, returned trends may include hashtags
			
		Returns and raises
		------------------
		See documentation for place()
		
		"""
		parameters = { 'id': 1 }
		if exclude_hashtags:
			parameters['exclude'] = 'hashtags'
		trends = self.place(parameters)
		while True:
			yield trends.next()

	def place(self, parameters):
		"""Generator of trends at place

		Parameters
		----------
		parameters : dict
			Names and values for the trends/place URL endpoint.
			See https://dev.twitter.com/docs/api/1.1/get/trends/place.

		Returns
		-------
		trends : dict
			Trend names/values.
			See https://dev.twitter.com/docs/api/1.1/get/trends/place.

		Raises
		------
		HTTP errors.

		"""
		try:
			params = urllib.urlencode(parameters)
			headers, content = self.client.request('%s?%s' % (API_ENDPOINT_URL_PLACE, params), 'GET')
			content = json.loads(content)
			if 'errors' in content:
				for error in content['errors']:
					yield error
			elif 'trends' in content[0]:
				for trend in content[0]['trends']:
					yield trend
		except IOError, e:
			if hasattr(e, 'reason'):
				raise Exception('Server unreachable: %s' % e.reason)
			elif hasattr(e, 'code'):
				raise Exception('Server cannot fulfill the request: %s' % e.code)

	def available(self):
		"""Generator of available trending places

		Returns
		-------
		trends : dict
			Place names/values.
			See https://dev.twitter.com/docs/api/1.1/get/trends/available.

		Raises
		------
		HTTP errors.

		"""
		try:
			headers, content = self.client.request(API_ENDPOINT_URL_AVAILABLE, 'GET')
			content = json.loads(content)
			if 'errors' in content:
				for error in content['errors']:
					yield error
			else:
				for place in content:
					yield place
		except IOError, e:
			if hasattr(e, 'reason'):
				raise Exception('Server unreachable: %s' % e.reason)
			elif hasattr(e, 'code'):
				raise Exception('Server cannot fulfill the request: %s' % e.code)
