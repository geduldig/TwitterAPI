"""
	REQUIRED: PASTE YOUR TWITTER OAUTH CREDENTIALS INTO puttytat/tools/credentials.txt 
	          OR USE -oauth OPTION TO USE A DIFFERENT FILE CONTAINING THE CREDENTIALS.
	
	Uploads a tweet.  Prints error on request failure.
"""

__author__ = "Jonas Geduldig"
__date__ = "January 15, 2013"
__license__ = "MIT"

# unicode printing for Windows 
import sys, codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import argparse
import os
import twitterapi

OAUTH = None

def update_timeline(message):
	update = twitterapi.TwUpdate(OAUTH)
	update.post({ 'status': message })
	print 'ok'

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Post a tweet.')
	parser.add_argument('-oauth', metavar='FILENAME', type=str, help='read OAuth credentials from file')
	parser.add_argument('message', metavar='TWEET', type=str, help='a message to post to timeline')
	args = parser.parse_args()	

	if args.oauth:
		OAUTH = twitterapi.TwCredentials.read_file(args.oauth)
	else:
		path = os.path.dirname(__file__)
		path = os.path.join(path, 'credentials.txt')
		OAUTH = twitterapi.TwCredentials.read_file(path)
	
	try:
		update_timeline(args.message)
	except Exception, e:
		print>>sys.stderr, '***', e
