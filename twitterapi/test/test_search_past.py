"""
	TEST SCRIPT

	REQUIRED: PASTE YOUR TWITTER OAUTH CREDENTIALS INTO credentials.txt.

	Downloads and prints past tweets containing 'zzz' in batches of 15.
	Waits 5 seconds between each batch.
	May also print warning messages.
	If the script is run more than 180 times in 15 minutes, prints a quota
	message (code=88) and terminates.
	Twitter will return tweets up to about a week old and then terminate
	the connection.
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

parameters = { 'q': 'zzz' }

search = twitterapi.TwSearch(oauth_credentials, parameters)

try:
	for item in search.past_results():
		if 'message' in item:
			print '\n\n\nMessage from twiter: %s\n\n\n' % item['message']
			if item['code'] == 88:
				quota = search.get_quota()
				print 'Suspend search until %s' % quota['reset']
				break
		else:
			print item['text']
except Exception, e:
	print e
