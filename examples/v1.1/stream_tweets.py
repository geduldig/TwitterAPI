from TwitterAPI import TwitterAPI

TRACK_TERM = 'pizza'

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

r = api.request('statuses/filter', {'track': TRACK_TERM})

for item in r:
    print(item['text'] if 'text' in item else item)