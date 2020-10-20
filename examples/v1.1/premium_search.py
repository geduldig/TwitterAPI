from TwitterAPI import TwitterAPI

SEARCH_TERM = 'pizza'
PRODUCT = '30day'
LABEL = 'your label'

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
                {'query':SEARCH_TERM})

for item in r:
    print(item['text'] if 'text' in item else item)
