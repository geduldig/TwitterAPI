# Twitter places several restrictions on uploaded video. If your upload fails
# with error 324, your video probably violates these restrictions.
#
# Read about them here:
# https://dev.twitter.com/rest/public/uploading-media#videorecs

from TwitterAPI import TwitterAPI
import os
import sys


VIDEO_FILENAME = 'test.mp4'
TWEET_TEXT = 'Video upload test'

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''


api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)


bytes_sent = 0
total_bytes = os.path.getsize(VIDEO_FILENAME)
file = open(VIDEO_FILENAME, 'rb')


def check_status(r):
	if r.status_code < 200 or r.status_code > 299:
		print(r.status_code)
		print(r.text)
		sys.exit(0)


r = api.request('media/upload', {'command':'INIT', 'media_type':'video/mp4', 'total_bytes':total_bytes})
check_status(r)

media_id = r.json()['media_id']
segment_id = 0

while bytes_sent < total_bytes:
  chunk = file.read(4*1024*1024)
  r = api.request('media/upload', {'command':'APPEND', 'media_id':media_id, 'segment_index':segment_id}, {'media':chunk})
  check_status(r)
  segment_id = segment_id + 1
  bytes_sent = file.tell()
  print('[' + str(total_bytes) + ']', str(bytes_sent))

r = api.request('media/upload', {'command':'FINALIZE', 'media_id':media_id})
check_status(r)

r = api.request('statuses/update', {'status':TWEET_TEXT, 'media_ids':media_id})
check_status(r)
