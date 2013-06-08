"""
	Beginning with Twitter's version 1.1 APIs, all requests require OAuth authentication.
	Simply log into dev.twitter.com, create an application, and generate your consumer
	key and secret and your access token key and secret.
	
	To use puttytat's classes, you will instantiate them with TwitterOauth which 
	contains your secrets and keys.  If you don't want to hard-code your credentials,
	you can store them in a text file and have TwitterOauth read them for you.  Save 
	your keys and secrets in a file, like this:
	
		consumer_key=YOUR_CONSUMER_KEY
		consumer_secret=YOUR_CONSUMER_SECRET
		access_token_key=YOUR_ACCESS_TOKEN_KEY
		access_token_secret=YOUR_ACCESS_TOKEN_SECRET
"""

__author__ = "Jonas Geduldig"
__date__ = "February 7, 2013"
__license__ = "MIT"

import os


class TwitterOauth:
	"""A container for Twitter's OAuth credentials"""

	def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_token_key = access_token_key
		self.access_token_secret = access_token_secret
		
	@classmethod
	def read_file(cls, file_name=None):
		"""Read OAuth credentials from a text file
		
		Parameter
		---------
		file_name : str
			Name of file containing a key-value pair on each line.  (No quotes around key or value.)
		
		"""
		if file_name is None:
			path = os.path.dirname(__file__)
			file_name = os.path.join(path, 'credentials.txt')

		with open(file_name) as f:
			oauth = {}
			for line in f:
				if '=' in line:
					name, value = line.split('=', 1)
					oauth[name.strip()] = value.strip()
			return TwitterOauth(
				oauth['consumer_key'], 
				oauth['consumer_secret'], 
				oauth['access_token_key'], 
				oauth['access_token_secret'])
