__author__ = "Jonas Geduldig"
__date__ = "June 8, 2013"
__license__ = "MIT"

import time
	

class TwitterRestPager(object):
	"""Simulates a stream iterator for REST API endpoints."""
	
	def __init__(self, api, resource, params=None):
		"""Initiate with an authenticated instance of TwitterAPI.
		
		api: The TwitterAPI instance.
		resource: Any REST API resource string.
		params: A dict containing parameters for the resource.
		"""		
		self.api = api
		self.resource = resource
		self.params = params

	def get_iterator(self, wait=5, new_tweets=False):
		"""Iterate through successive pages of results.  
		
		wait: Number of seconds wait between request to not exceed rate limit.
		      Depending on the resource, appropriate values are 5 or 60 seconds.
		new_tweets: Determines the direction in time (False: backwards, True: forwards).
		
		Returns a tweet status as a JSON structure.
		"""		
		while True:
			# get one page of results
			self.api._rest_request(self.resource, self.params)
			iter = self.api.get_iterator()
			if new_tweets:
				iter.results = reversed(iter.results)
				
			# yield each item in the page
			id = None
			for item in iter:
				if 'id' in item:
					id = item['id']
				yield item
				
			# sleep before getting another page of results
			time.sleep(wait)
			
			# use the first or last tweet id to limit (depending on the newer/older direction)
			# the next request
			if id is None:
				continue
			elif new_tweets:
				self.params['since_id'] = str(id)
			else:
				self.params['max_id'] = str(id - 1)