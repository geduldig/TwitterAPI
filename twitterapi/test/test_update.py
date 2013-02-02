"""
	TEST SCRIPT

	REQUIRED: PASTE YOUR TWITTER OAUTH CREDENTIALS INTO credentials.txt.

	Uploads a tweets containing 'zzz'.
	Prints error on request failure.
	May also print HTTP error.
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

parameters = { 'status': 'zzz' }

update = twitterapi.TwUpdate(oauth_credentials)

try:
	update.post(parameters)
	print 'ok'
except Exception, e:
	print e