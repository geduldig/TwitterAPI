"""
	TEST SCRIPT

	REQUIRED: PASTE YOUR TWITTER OAUTH CREDENTIALS INTO credentials.txt.

	Prints trending places in the US.  
	Then prints trends for all of US.
	If script is run more than 15 times in 15 minutes, prints a quota
	message (code=88).
"""

import twitterapi

# unicode printing for Windows 
import sys, codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

# read oauth credentials from file in module directory
import os
path = os.path.dirname(twitterapi.test.__file__)
path = os.path.join(path, 'credentials.txt')
oauth_credentials = twitterapi.TwCredentials.read_file(path)

COUNTRY = 'US'

trends = twitterapi.TwTrends(oauth_credentials)

try:
	# Print all trending places in the country and save the country's woeid.
	woeid = None
	name = None
	for item in trends.available():
		if 'message' in item:
			raise Exception('Message from twiter: %s' % item['message'])
		elif item['countryCode'] == COUNTRY:
			print item['name'], item['placeType']['name']
			if item['placeType']['name'] == 'Country':
				woeid = item['woeid']
				name = item['name']
	
	# Print trends for the country.			
	if woeid != None:
		print '\n%s trends:' % name
		parameters = { 'id': woeid, 'exclude': 'hashtags' }
		for item in trends.place(parameters):
			if 'message' in item:
				raise Exception('Message from twiter: %s' % item['message'])
			else:
				print item['name']
				
	# Print world-wide trends.
	print '\nWorld-wide trends:'
	for item in trends.worldwide():
		if 'message' in item:
			raise Exception('Message from twiter: %s' % item['message'])
		else:
			print item['name']
		
except Exception, e:
	print e
