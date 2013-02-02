__author__ = "Jonas Geduldig"
__date__ = "December 3, 2012"
__license__ = "MIT"

from datetime import datetime
import json
import oauth2 as oauth
import time
import urllib

API_ENDPOINT_URL = 'https://api.twitter.com/1.1/search/tweets.json'

class TwSearch:
	"""Accesses Twitter's REST API for searching tweets"""

	def __init__(self, oauth_credentials, parameters):
		"""Configure the search request

		Parameters
		----------
		oauth_credentials : TwCredentials
			The consumer and access token keys and secrets.
		parameters: dict
			Names and values for the search/tweets URL endpoint.
			See https://dev.twitter.com/docs/api/1.1/get/search/tweets.

		"""
		self.oauth_credentials = oauth_credentials
		self.parameters = parameters
		self.client = None
		self.headers = None
		self._setup_request()

	def _setup_request(self):
		oauth_token = oauth.Token(key=self.oauth_credentials.access_token_key, secret=self.oauth_credentials.access_token_secret)
		oauth_consumer = oauth.Consumer(key=self.oauth_credentials.consumer_key, secret=self.oauth_credentials.consumer_secret)
		self.client = oauth.Client(oauth_consumer, oauth_token)

	def get_quota(self):
		"""Parse quota information from HTTP header returned by Twitter

		Returns
		-------
		A dictionary containing the followig keys:
		remaining : int
			Number of requests available.
		limit: int
			Maximum number of requests allowed in 15 minutes.
		reset: datetime
			If limit exceeded, the time until when requests should suspend.

		"""		
		remaining = None
		limit = None
		reset = None
		if self.headers:
			if self.headers.has_key('x-rate-limit-remaining'):
				remaining = int(self.headers['x-rate-limit-remaining'])
				if remaining == 0:
					if self.headers.has_key('x-rate-limit-limit'):
						limit = int(self.headers['x-rate-limit-limit'])
					if self.headers.has_key('x-rate-limit-reset'):
						reset = int(self.headers['x-rate-limit-reset'])
						reset = datetime.fromtimestamp(reset)
		return { 'remaining': remaining, 'limit': limit, 'reset': reset }

	def results(self, forward=False):
		"""Generator of downloaded tweets

		Returns
		-------
		status : dict
			Status (tweet) name/values.
			See https://dev.twitter.com/docs/platform-objects/tweets.
		error : dict
			Error message name/values.
			See https://dev.twitter.com/docs/error-codes-responses.
			
		forward : bool
			If True, generate chronologically forward.

		Raises
		------
		HTTP errors.

		"""
		try: 
			params = urllib.urlencode(self.parameters)
			self.headers, content = self.client.request('%s?%s' % (API_ENDPOINT_URL, params), 'GET')
			content = json.loads(content)
			if 'statuses' in content:
				statuses = reversed(content['statuses']) if forward else content['statuses']
				for status in statuses:
					yield status
			elif 'errors' in content:
				for error in content['errors']:
					yield error
		except IOError, e: 
			if hasattr(e, 'reason'):
				raise Exception('Server unreachable: %s' % e.reason)
			elif hasattr(e, 'code'):
				raise Exception('Server cannot fulfill the request: %d' % e.code)

	def page_results(self, wait=5, forward=False):
		"""Generator of pages of downloaded tweets.  
		   Download either old tweets (default) or new tweets.
		   Default is 15 tweets per page with a 5 second wait between pages.

		Parameters
		----------
		wait : int
			Number of seconds between consecutive page requests.
			A value of 5 should prevent exceeding the 15-minute quota.
			
		forward : bool
			True returns new tweets in chronological order.
			False returns old tweets in reverse chronological order.

		Returns and Raises
		------------------
		See documentation for results().

		"""
		while True:
			id = None
			for item in self.results(forward):
				if item.has_key('id'):
					id = item['id']
				yield item
			time.sleep(wait)
			if id == None:
				break
			elif forward:
				self.parameters['since_id'] = str(id)
			else:
				self.parameters['max_id'] = str(id - 1)
				
	def past_results(self, wait=5):
		"""Generator of downloaded old tweets in reverse chronological order

		Parameters
		----------
		wait : int
			Number of seconds between consecutive page requests.
			A value of 5 should prevent exceeding the 15-minute quota.

		Returns and Raises
		------------------
		See documentation for results().

		"""
		for item in self.page_results(wait, False):
			yield item
			
	def new_results(self, wait=5):
		"""Generator of downloaded new tweets in chronological order

		Parameters
		----------
		wait : int
			Number of seconds between consecutive page requests.
			A value of 5 should prevent exceeding the 15-minute quota.

		Returns and Raises
		------------------
		See documentation for results().

		"""
		for item in self.page_results(wait, True):
			yield item