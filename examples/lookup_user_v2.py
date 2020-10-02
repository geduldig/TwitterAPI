# Documentation
# https://documenter.getpostman.com/view/9956214/T1LMiT5U#auth-info-784efcda-ed4c-4491-a4c0-a26470a67400

# You must opt-in to v2 here:
# https://developer.twitter.com/en/portal/opt-in

from TwitterAPI import TwitterAPI, TwitterPager

SCREEN_NAME = 'TheTweetOfGod'

api = TwitterAPI(<consumer_key>, 
                 <consumer_secret>,
                 auth_type='oAuth2')

r = api.request(f'users/by/username/:{SCREEN_NAME}', version='2')
print(r.json()['data']['id'] if r.status_code == 200 else 'PROBLEM: ' + r.text)
