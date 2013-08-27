"""
	This command line script can be run with any Twitter endpoint.  The json-formatted
	response is printed to the console.  The script works with both Streaming API and
	REST API endpoints.

	IMPORTANT: Before using this script, you must enter your Twitter application's OAuth 
	credentials in TwitterAPI/credentials.txt.  Log into to dev.twitter.com to create 
	your application.
	
	Examples:
	
	> python cli.py -endpoint search/tweets -parameters q=zzz 
	> python cli.py -endpoint statuses/filter -parameters track=zzz
		
	These examples print the raw json response.  You can also print one or more fields
	from the response, for instance the tweet 'text' field, like this:
	
	> python cli.py -endpoint statuses/filter -parameters track=zzz -fields text
		
	Twitter's endpoints are documented at this site:
		https://dev.twitter.com/docs/api/1.1
"""

__author__ = "Jonas Geduldig"
__date__ = "June 7, 2013"
__license__ = "MIT"

import argparse
import codecs
from pprint import PrettyPrinter
import sys
from .TwitterOAuth import TwitterOAuth
from .TwitterAPI import TwitterAPI


try:
	# python 3
	sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
	sys.stderr = codecs.getwriter('utf8')(sys.stderr.buffer)
except:
	# python 2
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	sys.stderr = codecs.getwriter('utf8')(sys.stderr)


def find_field(name, obj):
	"""Breadth-first search of the JSON result fields."""
	q = []
	q.append(obj)
	while q:
		obj = q.pop(0)
		if hasattr(obj, '__iter__'):
			isdict = type(obj) is dict
			if isdict and name in obj:
				return obj[name]
			for k in obj:
				q.append(obj[k] if isdict else k)
	else:
		return None


def to_dict(param_list):
	"""Convert a list of key=value to dict[key]=value"""			
	if param_list is not None:
		return {name: value for (name, value) in [param.split('=') for param in param_list]}
	else:
		return None


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Request any Twitter Streaming or REST API endpoint')
	parser.add_argument('-oauth', metavar='FILENAME', type=str, help='file containing OAuth credentials')
	parser.add_argument('-endpoint', metavar='ENDPOINT', type=str, help='Twitter endpoint', required=True)
	parser.add_argument('-parameters', metavar='NAME_VALUE', type=str, help='parameter NAME=VALUE', nargs='+')
	parser.add_argument('-fields', metavar='FIELD', type=str, help='print a top-level field in the json response', nargs='+')
	args = parser.parse_args()	

	try:
		params = to_dict(args.parameters)
		oauth = TwitterOAuth.read_file(args.oauth)

		api = TwitterAPI(oauth.consumer_key, oauth.consumer_secret, oauth.access_token_key, oauth.access_token_secret)
		api.request(args.endpoint, params)
		iter = api.get_iterator()
		
		pp = PrettyPrinter()
		for item in iter:
			if 'message' in item:
				sys.stdout.write('ERROR %s: %s\n' % (item['code'], item['message']))
				sys.stdout.flush()
			elif args.fields is None:
				pp.pprint(item)
				sys.stdout.flush()
			else:
				for name in args.fields:
					value = find_field(name, item)
					if value is not None:
						sys.stdout.write('%s: %s\n' % (name, value))
						sys.stdout.flush()
						
	except KeyboardInterrupt:
		sys.stderr.write('\nTerminated by user\n')
		
	except Exception as e:
		sys.stderr.write('*** STOPPED %s\n' % str(e))