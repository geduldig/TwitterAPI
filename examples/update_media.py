from TwitterAPI import TwitterAPI


TWEET_TEXT = 'some tweet text'
IMAGE_PATH = './some_image.png'


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''


api = TwitterAPI(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET)

file = open(IMAGE_PATH, 'rb')
data = file.read()
r = api.request('media/upload', None, {'media': data})
print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

if r.status_code == 200:
	media_id = r.response.json()['media_id']
	r = api.request('statuses/update', {'status':TWEET_TEXT, 'media_ids':media_id})
	print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')
