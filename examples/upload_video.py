from TwitterAPI import TwitterAPI
import os
import sys

MOVIE = 'test.mp4'
TWEET_TEXT = 'my movie uploaded!'

nbytes = os.path.getsize(MOVIE)
file = open(MOVIE, 'rb')
data = file.read()

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''

api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)

def check_status(r):
	if r.status_code < 200 or r.status_code > 299:
		print(r.status_code)
		print(r.text)
		sys.exit(0)

r = api.request('media/upload', {'command':'INIT', 'media_type':'video/mp4', 'total_bytes':nbytes})
check_status(r.status_code)

media_id = r.json()['media_id']
r = api.request('media/upload', {'command':'APPEND', 'media_id':media_id, 'segment_index':0}, {'media':data})
check_status(r.status_code)

r = api.request('media/upload', {'command':'FINALIZE', 'media_id':media_id})
check_status(r.status_code)

r = api.request('statuses/update', {'status':TWEET_TEXT, 'media_ids':media_id})
check_status(r.status_code)
