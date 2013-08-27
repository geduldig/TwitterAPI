__author__ = "Jonas Geduldig"
__date__ = "June 7, 2013"
__license__ = "MIT"

from .constants import *
import json
import requests
from requests_oauthlib import OAuth1


class TwitterAPI(object):	
	"""Access any REST or Streaming API resource.  
	
	Valid resource strings are found in constants.py.  Documentation and parameters for 
	each resource here: https://dev.twitter.com/docs/api/1.1
	"""

	def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
		self.session = requests.Session() 
		self.session.auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
		self.session.headers = {'User-Agent':USER_AGENT}
		
	def _make_url(self, subdomain, path):
		return '%s://%s.%s/%s/%s' % (PROTOCOL, subdomain, DOMAIN, VERSION, path)
		
	def _rest_request(self, resource, params=None):
		method = REST_ENDPOINTS[resource][0]
		url = self._make_url(REST_SUBDOMAIN, resource + '.json')
		self.session.stream = False
		self.response = self.session.request(method, url, params=params, timeout=REST_SOCKET_TIMEOUT)
		return self.response
		
	def _streaming_request(self, resource, params=None):
		method = 'GET' if params is None else 'POST'
		url = self._make_url(STREAMING_ENDPOINTS[resource][0], resource + '.json')
		self.session.stream = True
		self.response = self.session.request(method, url, params=params, timeout=STREAMING_SOCKET_TIMEOUT)
		return self.response
		
	def request(self, resource, params=None):
		"""Request any Twitter resource.
		
		resource: A REST or Streaming API resource string (ex 'search/tweets').
		params: Dictionary of resource parameters (ex {'q':'zzz, 'count':10}).
		
		Returns a response object from the requests module.  
		"""
		if resource in REST_ENDPOINTS:
			return self._rest_request(resource, params)
		elif resource in STREAMING_ENDPOINTS:
			return self._streaming_request(resource, params)
		else:
			raise Exception('"%s" is not valid endpoint' % resource)
			
	def get_iterator(self):
		"""Returns the appropriate iterator for either a REST or Streaming API request."""
		if self.session.stream:
			return StreamingIterator(self.response)
		else:
			return RestIterator(self.response)

	def get_rest_quota(self):
		"""Returns quota information from the response header of a REST API request."""
		remaining, limit, reset = None, None, None
		if self.response and not self.session.stream:
			if 'x-rate-limit-remaining' in self.response.headers:
				remaining = int(self.response.headers['x-rate-limit-remaining'])
				if remaining == 0:
					limit = int(self.response.headers['x-rate-limit-limit'])
					reset = int(self.response.headers['x-rate-limit-reset'])
					reset = datetime.fromtimestamp(reset)
		return {'remaining': remaining, 'limit': limit, 'reset': reset}

				
class RestIterator(object):
	def __init__(self, response):
		"""Extracts from the response the parts that can be iterated."""
		resp = response.json()
		if 'errors' in resp:
			self.results = resp['errors']
		elif 'statuses' in resp:
			self.results = resp['statuses']
		elif hasattr(resp, '__iter__') and type(resp) is not dict:
			if len(resp) > 0 and 'trends' in resp[0]:
				self.results = resp[0]['trends']
			else:
				self.results = resp
		else:		
			self.results = (resp,)
		
	def __iter__(self):
		"""Returns a tweet status as a JSON object."""
		for item in self.results:
			yield item
				
				
class StreamingIterator(object):
	def __init__(self, response):
		self.results = response.iter_lines()
		
	def __iter__(self):
		"""Returns a tweet status as a JSON object."""
		for item in self.results:
			if item:
				yield json.loads(item.decode('utf-8'))
