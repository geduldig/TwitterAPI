from TwitterAPI import TwitterAPI

SCREEN_NAME = 'TheTweetOfGod'

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 auth_type='oAuth2')

r = api.request('users/lookup', {'screen_name':SCREEN_NAME})
print(r.json()[0]['id'] if r.status_code == 200 else 'PROBLEM: ' + r.text)
