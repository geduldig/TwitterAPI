"""
	REQUIRED: PASTE YOUR TWITTER OAUTH CREDENTIALS INTO puttytat/tools/credentials.txt 
	          OR USE -oauth OPTION TO USE A DIFFERENT FILE CONTAINING THE CREDENTIALS.
	
	Downloads old or new tweets that contain any of the words that are passed as 
	arguments on the command line.  Prints just the tweet text.
	
	By default, downloads old tweets.  To get just new tweets, use the -new flag.
	
	By default, downloads 15 tweets at a time.  Use the -count option to override.
	
	The script calls Twitter's REST API which permits about a week's worth of old 
	tweets to be downloaded before quitting the connection.  Twitter may also 
	disconnect if you exceed 180 downloads per 15 minutes.  For this reason sleep is 
	called after each request.  The default is 5 seconds.  Override with the '-wait' 
	option.
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

def search_tweets(list, count, new, wait):
	words = ' OR '.join(list)
	params = { 'q': words }
	if count != None:
		params['count'] = count
	search = twitterapi.TwSearch(OAUTH, params)
	while True:
		for item in search.page_results(wait, new):
			if 'text' in item:
				print item['text']
			elif 'message' in item:
				if item['code'] == 131:
					continue # ignore internal server error
				elif item['code'] == 88:
					print>>sys.stderr, 'Suspend search until %s' % search.get_quota()['reset']
				raise Exception('Message from twiter: %s' % item['message'])

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Search tweet history or current tweets.')
	parser.add_argument('-oauth', metavar='FILENAME', type=str, help='read OAuth credentials from file')
	parser.add_argument('-count', type=int, help='number of tweets per download')
	parser.add_argument('-wait', type=int, default=5, help='seconds to wait between downloads')
	parser.add_argument('-new', action='store_true', help='download only new tweets')
	parser.add_argument('words', metavar='W', type=str, nargs='+', help='a word to track')
	args = parser.parse_args()	

	if args.oauth:
		OAUTH = twitterapi.TwCredentials.read_file(args.oauth)
	else:
		path = os.path.dirname(__file__)
		path = os.path.join(path, 'credentials.txt')
		OAUTH = twitterapi.TwCredentials.read_file(path)
	
	try:
		search_tweets(args.words, args.count, args.new, args.wait)
	except KeyboardInterrupt:
		print>>sys.stderr, '\nTerminated by user'
	except Exception, e:
		print>>sys.stderr, '*** STOPPED', e
