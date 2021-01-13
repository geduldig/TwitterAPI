from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError
from pprint import pprint

USER_ID = '2244994945'  # https://twitter.com/TwitterDev

try:
    o = TwitterOAuth.read_file()
    api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret, api_version='2')

    # Get tweets - default setting
    tweets = api.request(f'users/:{USER_ID}/tweets')
    for t in tweets:
        print(t)

    # Get tweets with customization - (5 tweets only with created_at timestamp)
    print()
    params = {'max_results': 5, 'tweet.fields': 'created_at'}
    tweets = api.request(f'users/:{USER_ID}/tweets', params)
    for t in tweets:
        pprint(t)
        
    # Get next 5 tweets
    print()
    next_token = tweets.json()['meta']['next_token']
    params = {'max_results': 5, 'tweet.fields': 'created_at', 'pagination_token': next_token}
    tweets = api.request(f'users/:{USER_ID}/tweets', params)
    for t in tweets:
        pprint(t)    
    
        
except TwitterRequestError as e:
    print('Request error')
    print(e.status_code)
    for msg in iter(e):
        print(msg)

except TwitterConnectionError as e:
    print('Connection error')
    print(e)

except Exception as e:
    print('Exception')
    print(e)