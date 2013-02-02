__author__ = "Jonas Geduldig"
__date__ = "December 3, 2012"
__license__ = "MIT"

class TwCredentials:
	"""A container for Twitter's OAuth credentials"""

	def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret, application_name=None):
		"""application_name is optional but useful to remember what account these credentials belong to."""
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_token_key = access_token_key
		self.access_token_secret = access_token_secret
		self.application_name = application_name
		
	@classmethod
	def read_file(cls, file_name):
		"""Read OAuth credentials from a text file
		
		Parameter
		---------
		file_name : str
			Name of file containing a key-value pair on each line.  (No quotes around key or value.)
		
		"""
		c = { 
			'consumer_key': None, 
			'consumer_secret': None, 
			'access_token_key': None, 
			'access_token_secret': None, 
			'application_name': None 
		}
		with open(file_name) as f:
			for line in f:
				kv = line.split('=')
				if len(kv) == 2:
					c[kv[0].strip()] = kv[1].strip()
		return TwCredentials(
					c['consumer_key'], 
					c['consumer_secret'], 
					c['access_token_key'], 
					c['access_token_secret'], 
					c['application_name'])
