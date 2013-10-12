__author__ = "Jonas Geduldig"
__date__ = "June 7, 2013"
__license__ = "MIT"

from .constants import *
import json
import requests
from requests_oauthlib import OAuth1


class TwitterAPI(object):	
	"""Access REST API or Streaming API resources."""
	
	def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
		self.auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
				
	def _prepare_url(self, subdomain, path):
		return '%s://%s.%s/%s/%s.json' % (PROTOCOL, subdomain, DOMAIN, VERSION, path)
		
	def _get_endpoint(self, resource):
		""" Substitute parameters in the resource path with :PARAM."""
		if ':' in resource:
			parts = resource.split('/')
			# embedded parameters start with ':'
			parts = [k if k[0] != ':' else ':PARAM' for k in parts]
			endpoint = '/'.join(parts)
			resource = resource.replace(':', '')
			return (resource, endpoint)
		else:
			return (resource, resource)
	
	def request(self, resource, params=None):
		"""Return a TwitterResponse object."""
		session = requests.Session() 
		session.auth = self.auth
		session.headers = {'User-Agent':USER_AGENT}
		resource, endpoint = self._get_endpoint(resource)
		if endpoint in STREAMING_ENDPOINTS:
			session.stream = True
			method = 'GET' if params is None else 'POST'
			url = self._prepare_url(STREAMING_ENDPOINTS[endpoint][0], resource)
			timeout = STREAMING_SOCKET_TIMEOUT
		elif endpoint in REST_ENDPOINTS:
			session.stream = False
			method = REST_ENDPOINTS[endpoint][0]
			url = self._prepare_url(REST_SUBDOMAIN, resource)
			timeout = REST_SOCKET_TIMEOUT
		else:
			raise Exception('"%s" is not valid endpoint' % resource)
		r = session.request(method, url, params=params, timeout=timeout)
		return TwitterResponse(r, session.stream)


class TwitterResponse(object):
	"""Response from either a REST API or Streaming API resource call."""
	
	def __init__(self, response, stream):
		"""Args: 
			requests.Response object 
			boolean, True if streaming connection
		"""
		self.response = response
		self.stream = stream

	@property
	def status_code(self):
		return self.response.status_code

	@property
	def text(self):
		return self.response.text

	def get_iterator(self):
		if self.stream:
			return StreamingIterator(self.response) 
		else:
			return RestIterator(self.response)
		
	def __iter__(self):
		for item in self.get_iterator():
			yield item

	def get_rest_quota(self):
		"""Return quota information from the response header of a REST API request."""
		remaining, limit, reset = None, None, None
		if self.response:
			if 'x-rate-limit-remaining' in self.response.headers:
				remaining = int(self.response.headers['x-rate-limit-remaining'])
				if remaining == 0:
					limit = int(self.response.headers['x-rate-limit-limit'])
					reset = int(self.response.headers['x-rate-limit-reset'])
					reset = datetime.fromtimestamp(reset)
		return {'remaining': remaining, 'limit': limit, 'reset': reset}

				
class RestIterator(object):
	def __init__(self, response):
		"""Extract iterable parts from the response."""
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
		"""Return a tweet status as a JSON object."""
		for item in self.results:
			if item:
				yield json.loads(item.decode('utf-8'))

