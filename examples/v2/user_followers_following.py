from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError

USER_ID = '2244994945'  # https://twitter.com/TwitterDev

try:
    o = TwitterOAuth.read_file()
    api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret, api_version='2')
    
    # Get followers
    followers = api.request(f'users/:{USER_ID}/followers')
    for f in followers:
        print(f)
    
    # Get following
    following = api.request(f'users/:{USER_ID}/following')
    for f in following:
        print(f)

except TwitterRequestError as e:
    print(e.status_code)
    for msg in iter(e):
        print(msg)

except TwitterConnectionError as e:
    print(e)

except Exception as e:
    print(e)
