from TwitterAPI import TwitterAPI
 
TWEET_TEXT = 'some tweet text'

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)
 
r = api.request('statuses/update', {'status':TWEET_TEXT})
print(r.status_code)