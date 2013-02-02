__author__ = "Jonas Geduldig"
__date__ = "December 3, 2012"
__license__ = "MIT"

import json
import oauth2 as oauth
import socket
import time
import urllib
import urllib2

API_ENDPOINT_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
DEFAULT_USER_AGENT = 'TwitterAPI'
SOCKET_TIMEOUT = 90 # 90 seconds per Twitter's recommendation

class TwStream:
	"""Accesses Twitter's Streaming API for filtering tweets"""

	user_agent = DEFAULT_USER_AGENT 

	def __init__(self, oauth_credentials, parameters):
		"""Configure the streaming request

		Parameters
		----------
		oauth_credentials : TwCredentials
			The consumer and access token keys and secrets.
		parameters: dict
			Names and values for the search/tweets URL endpoint.
			See https://dev.twitter.com/docs/api/1.1/post/statuses/filter.

		"""
		self.oauth_credentials = oauth_credentials
		self.parameters = urllib.urlencode(parameters)
		self.headers = None
		self._setup_request()

	def _setup_request(self):
		oauth_token = oauth.Token(key=self.oauth_credentials.access_token_key, secret=self.oauth_credentials.access_token_secret)
		oauth_consumer = oauth.Consumer(key=self.oauth_credentials.consumer_key, secret=self.oauth_credentials.consumer_secret)
		oauth_params = {
			'oauth_version': '1.0',
			'oauth_nonce': oauth.generate_nonce(),
			'oauth_timestamp': int(time.time())
		}
		req = oauth.Request(method='POST', parameters=oauth_params, url='%s?%s' % (API_ENDPOINT_URL, self.parameters))
		req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), oauth_consumer, oauth_token)
		oauth_header = req.to_header()['Authorization'].encode('utf-8')
		self.headers = {
			'User-Agent': self.user_agent,
			'Content-Type': 'application/x-www-form-urlencoded',
			'Authorization': oauth_header
		}

	def results(self):
		"""Generator of downloaded tweets

		Returns
		-------
		status : dict
			Status (tweet) name/values.
			See https://dev.twitter.com/docs/platform-objects/tweets.
		message(s) : dict
			A variety of possible message types, including the 'limit'
			message to notify how many tweets have been skipped.
			See https://dev.twitter.com/docs/streaming-apis/messages.

		Raises
		------
		HTTP errors and socket errors.  Client should reconnect on catch.

		"""
		END_OF_ITEM = '\r\n'
		try: 
			socket.setdefaulttimeout(SOCKET_TIMEOUT)
			req = urllib2.Request(API_ENDPOINT_URL, self.parameters, self.headers)
			resp = urllib2.urlopen(req)
			buffer = ''
			while True:
				chunk = resp.read(1);
				if not chunk:
					break # lost connection
				buffer += unicode(chunk)
				if END_OF_ITEM in buffer:
					first_item, buffer = buffer.split(END_OF_ITEM, 1)
					if first_item != '':
						item = json.loads(first_item)
						yield item
		except IOError, e:
			if hasattr(e, 'reason'):
				raise Exception('Server unreachable: %s' % e.reason)
			elif hasattr(e, 'code'):
				raise Exception('Server cannot fulfill the request: %d' % e.code)
