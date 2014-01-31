from TwitterAPI import TwitterAPI, TwitterOAuth


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''

# Using OAuth 1.0 to authenticate you have access all Twitter endpoints.
api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

# Using OAuth 2.0 to authenticate you lose access to user specific endpoints (ex. statuses/update).
#api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, auth_type="oAuth2")

# If you are behind a firewall you may need to provide proxy server authentication.
#api.set_proxy_url('https://USERNAME:PASSWORD@PROXYSERVER:PORT')


r = api.request('account/verify_credentials')


# Print HTTP status code (=200 when no errors).
print(r.status_code)

# Print the raw response.
print(r.text)

# Parse the JSON response.
j = r.response.json()
print('Authenticated account: %s' % j['screen_name'])
print('%s friends, %s followers' % (j['friends_count'], j['followers_count']))
