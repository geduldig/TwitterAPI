# You must opt-in to v2 here:
# https://developer.twitter.com/en/portal/opt-in

from TwitterAPI import TwitterAPI

TWEET_ID = '964575983633252353'

api = TwitterAPI(<consumer_key>, 
                 <consumer_secret>,
                 auth_type='oAuth2')

r = api.request(f'tweets/:{TWEET_ID}' , version='2')
tweet = r.json()
print(f"{tweet['data']['id']}: {tweet['data']['text']}" if r.status_code == 200 
      else f"PROBLEM: {r.text}")
