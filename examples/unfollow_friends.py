'''
Unfollow friends that do not follow you.
'''


from TwitterAPI import TwitterAPI


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN,
                 ACCESS_TOKEN_SECRET)


followers = set(id for id in api.request('followers/ids'))
friends = set(id for id in api.request('friends/ids'))
unfollow = set(followers) - set(friends)


for id in unfollow:
    r = api.request('friendships/destroy', {'user_id': id})
    if r.status_code == 200:
        status = r.json()
        print 'unfollowed %s' % status['screen_name']
