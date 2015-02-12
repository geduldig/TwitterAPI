'''
This example replaces post_image.py. It demonstrates a method for
posting an image, which now requires two API calls. 
'''

from TwitterAPI import TwitterAPI


TWEET_TEXT = 'some tweet text'
IMAGE_PATH = './some_image.png'


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''


api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)

# STEP 1 - upload image
file = open(IMAGE_PATH, 'rb')
data = file.read()
r = api.request('media/upload', None, {'media': data})
print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

# STEP 2 - post tweet with a reference to uploaded image
if r.status_code == 200:
    media_id = r.json()['media_id']
    r = api.request(
        'statuses/update', {'status': TWEET_TEXT, 'media_ids': media_id})
    print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')
