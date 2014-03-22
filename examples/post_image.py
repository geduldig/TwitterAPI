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
r = api.request('statuses/update_with_media',
                {'status': TWEET_TEXT},
                {'media[]': data})

print('SUCCESS' if r.status_code == 200 else 'FAILURE')
