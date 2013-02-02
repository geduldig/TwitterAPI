"""
	TEST SCRIPT

	REQUIRED: PASTE YOUR TWITTER OAUTH CREDENTIALS INTO credentials.txt.

	Downloads and prints stream of real-time tweets containing 'zzz'.
	May also print limit or disconnect messages.
	Stream continues forever or until a disconnect message or 
	until a HTTP error.
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

parameters = { 'track': 'zzz' }

stream = twitterapi.TwStream(oauth_credentials, parameters)

while True:
	try:
		for item in stream.results():
			if 'text' in item:
				print item['text']
			elif 'limit' in item:
				print '\n\n\nSkipped %s tweets\n\n\n' % item['limit'].get('track')
			elif 'disconnect' in item:
				raise Exception('Disconnect: %s' % item['disconnect'].get('reason'))
	except KeyboardInterrupt:
		print '\nTerminated by user'
		break
	except Exception, e:
		print e
		break
