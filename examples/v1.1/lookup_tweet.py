from TwitterAPI import TwitterAPI

TWEET_ID = '964575983633252353'

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 auth_type='oAuth2')

r = api.request('statuses/show/:' + TWEET_ID)
tweet = r.json()
print(tweet['user']['screen_name'] + ':' + tweet['text'] if r.status_code == 200 
      else 'PROBLEM: ' + r.text)