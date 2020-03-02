# Unfollow friends that do not follow you.

from TwitterAPI import TwitterAPI

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

followers = set(id for id in api.request('followers/ids'))
friends = set(id for id in api.request('friends/ids'))
unfollow = set(followers) - set(friends)

for id in unfollow:
    r = api.request('friendships/destroy', {'user_id': id})
    if r.status_code == 200:
        status = r.json()
        print 'unfollowed %s' % status['screen_name']