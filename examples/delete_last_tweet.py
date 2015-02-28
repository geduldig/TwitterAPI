from threading import Thread
from TwitterAPI import TwitterAPI

NUMBER_OF_TWEETS_TO_DELETE = 1

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)


class DeleteTweet(Thread):

    def __init__(self, tweet_id, count):
        Thread.__init__(self)
        self.tweet_id = tweet_id
        self.count = count

    def run(self):
        r = api.request('statuses/destroy/:%d' % self.tweet_id)
        print(self.count if r.status_code == 200 else r.text)

try:
    count = 0
    r = api.request(
        'statuses/user_timeline', {'count': NUMBER_OF_TWEETS_TO_DELETE})
    for item in r:
        if 'id' in item:
            count += 1
            tweet_id = item['id']
            DeleteTweet(tweet_id, count).start()
        else:
            raise Exception(item)
except Exception as e:
    print('Stopping: %s' % str(e))
