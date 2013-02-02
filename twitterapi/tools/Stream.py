"""
	REQUIRED: PASTE YOUR TWITTER OAUTH CREDENTIALS INTO puttytat/tools/credentials.txt 
	          OR USE -oauth OPTION TO USE A DIFFERENT FILE CONTAINING THE CREDENTIALS.
	
	Downloads real-time tweets that contain any of the words that are passed as 
	arguments on the command line.  Prints just the tweet text.
	
	The script calls Twitter's Streaming API which is bandwidth limitted.  If you 
	exceed the rate limit, Twitter sends a message with the total number of tweets 
	skipped during the current connection.  This number is printed, and the connection 
	remains open.
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

def stream_tweets(list):
	words = ','.join(list)
	while True:
		stream = twitterapi.TwStream(OAUTH, { 'track': words })
		try:
			while True:
				for item in stream.results():
					if 'text' in item:
						print item['text']
					elif 'disconnect' in item:
						raise Exception('Disconnect: %s' % item['disconnect'].get('reason'))
		except Exception, e:
			# reconnect on 401 errors and socket timeouts
			print>>sys.stderr, '*** MUST RECONNECT', e

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Get real-time tweet stream.')
	parser.add_argument('-oauth', metavar='FILENAME', type=str, help='read OAuth credentials from file')
	parser.add_argument('words', metavar='W', type=str, nargs='+', help='a word to track')
	args = parser.parse_args()	

	if args.oauth:
		OAUTH = twitterapi.TwCredentials.read_file(args.oauth)
	else:
		path = os.path.dirname(__file__)
		path = os.path.join(path, 'credentials.txt')
		OAUTH = twitterapi.TwCredentials.read_file(path)
	
	try:
		stream_tweets(args.words)
	except KeyboardInterrupt:
		print>>sys.stderr, '\nTerminated by user'
