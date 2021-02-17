# Unfollow friends that do not follow you.

from TwitterAPI import TwitterAPI

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

friends = set(id for id in api.request('friends/ids'))
followers = set(id for id in api.request('followers/ids'))
unfollow = set(friends) - set(followers)

for id in unfollow:
    r = api.request('friendships/destroy', {'user_id': id})
    if r.status_code == 200:
        status = r.json()
        print 'unfollowed %s' % status['screen_name']
