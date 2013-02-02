"""
	REQUIRED: PASTE YOUR TWITTER OAUTH CREDENTIALS INTO puttytat/tools/credentials.txt 
	          OR USE -oauth OPTION TO USE A DIFFERENT FILE CONTAINING THE CREDENTIALS.
	
	Prints woeid and name of trending places in the world.  
	
	Use option -woeid to supply a woeid and retrieve trends for that place.

	If script is run more than 15 times in 15 minutes, prints a quota message (code=88).
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

def trending_places():
	trends = twitterapi.TwTrends(OAUTH)
	for item in trends.available():
		if 'message' in item:
			raise Exception('Message from twiter: %s' % item['message'])
		else:
			print item['woeid'], item['name'], item['placeType']['name']

def trends_at_place(woeid):
	trends = twitterapi.TwTrends(OAUTH)
	for item in trends.place({ 'id': woeid }):
		if 'message' in item:
			raise Exception('Message from twiter: %s' % item['message'])
		else:
			print item['name']

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Get trending places or trends for a place.')
	parser.add_argument('-oauth', metavar='FILENAME', type=str, help='read OAuth credentials from file')
	parser.add_argument('-woeid', type=str, help='id of a trending place')
	args = parser.parse_args()	

	if args.oauth:
		OAUTH = twitterapi.TwCredentials.read_file(args.oauth)
	else:
		path = os.path.dirname(__file__)
		path = os.path.join(path, 'credentials.txt')
		OAUTH = twitterapi.TwCredentials.read_file(path)
	
	try:
		if args.woeid != None:
			trends_at_place(args.woeid)
		else:
			trending_places()
	except Exception, e:
		print>>sys.stderr, '***', e
