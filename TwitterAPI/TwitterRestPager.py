__author__ = "Jonas Geduldig"
__date__ = "June 8, 2013"
__license__ = "MIT"

import time
	

class TwitterRestPager(object):
	"""Pagination iterator for REST API resources"""
	
	def __init__(self, api, resource, params=None):
		"""Initialize with an authenticated instance of TwitterAPI
		
		:param api: A TwitterAPI object 
		:param resource: A string with the resource path (ex. search/tweets)
		:param params: A dict of resource parameters
		"""		
		self.api = api
		self.resource = resource
		self.params = params

	def get_iterator(self, wait=5, new_tweets=False):
		"""Gets an iterator for the data returned by Twitter
		
		:param wait: An integer number of seconds wait between requests 
		             (depending on the resource, appropriate values are 5 or 60 seconds)
		:param new_tweets: A bool determining the search direction 
		                   (False: old results, True: current results)
		
		:returns: A JSON object representing the return value
		"""		
		elapsed = 0
		while True:
			# get one page of results
			start = time.time()
			req = self.api.request(self.resource, self.params)
			iter = req.get_iterator()
			if new_tweets:
				iter.results = reversed(iter.results)
				
			# yield each item in the page
			id = None
			for item in iter:
				if 'id' in item:
					id = item['id']
				yield item
				
			# sleep before getting another page of results
			elapsed = time.time() - start
			pause = wait - elapsed if elapsed < wait else 0;
			time.sleep(pause)
			
			# use the first or last tweet id to limit (depending on the newer/older direction)
			# the next request
			if id is None:
				continue
			elif new_tweets:
				self.params['since_id'] = str(id)
			else:
				self.params['max_id'] = str(id - 1)