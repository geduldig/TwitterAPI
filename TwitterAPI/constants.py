"""
	Constants For All Twitter Endpoints
	-----------------------------------
	
	Version 1.1, Streaming API and REST API.
	
	URLs for each endpoint are composed of the following pieces:
		PROTOCOL://{subdomain}.DOMAIN/VERSION/{resource}?{parameters}
"""


__author__ = "geduldig"
__date__ = "February 3, 2012"
__license__ = "MIT"


PROTOCOL = 'https'
DOMAIN = 'twitter.com'


VERSION = '1.1'
CURATOR_VERSION = 'broadcast/1'
ADS_VERSION = '10'


ENDPOINTS = {
    # resource:                                             (method(s),        subdomain)

    # STREAMING API

    'statuses/filter':                                      ('POST',           'stream'),
    'statuses/firehose':                                    ('GET',            'stream'),
    'statuses/sample':                                      ('GET',            'stream'),
    'site':                                                 ('GET',            'sitestream'),
    'user':                                                 ('GET',            'userstream'),

    # PUBLIC API

    'account/remove_profile_banner':                        ('POST',           'api'),
    'account/settings':                                     ('GET',            'api'),
    'account/update_delivery_device':                       ('POST',           'api'),
    'account/update_profile':                               ('POST',           'api'),
    'account/update_profile_background_image':              ('POST',           'api'),
    'account/update_profile_banner':                        ('POST',           'api'),
    'account/update_profile_colors':                        ('POST',           'api'),
    'account/update_profile_image':                         ('POST',           'api'),
    'account/verify_credentials':                           ('GET',            'api'),
        
    'application/rate_limit_status':                        ('GET',            'api'),

    'blocks/create':                                        ('POST',           'api'),
    'blocks/destroy':                                       ('POST',           'api'),
    'blocks/ids':                                           ('GET',            'api'),
    'blocks/list':                                          ('GET',            'api'),

    'direct_messages':                                      ('GET',            'api'), # deprecated
    'direct_messages/destroy':                              ('POST',           'api'), # deprecated
    'direct_messages/events/destroy':                       ('DELETE',         'api'),
    'direct_messages/events/new':                           ('POST',           'api'),
    'direct_messages/events/list':                          ('GET',            'api'),
    'direct_messages/events/show':                          ('GET',            'api'),    
    'direct_messages/indicate_typing':                      ('POST',           'api'),
    'direct_messages/new':                                  ('POST',           'api'), # deprecated
    'direct_messages/sent':                                 ('GET',            'api'), # deprecated
    'direct_messages/show':                                 ('GET',            'api'), # deprecated
    'direct_messages/welcome_messages/new':                 ('POST',           'api'),
    'direct_messages/welcome_messages/list':                ('GET',            'api'),
    'direct_messages/welcome_messages/show':                ('GET',            'api'),
    'direct_messages/welcome_messages/destroy':             ('DELETE',         'api'),    
    'direct_messages/welcome_messages/rules/new':           ('POST',           'api'),
    'direct_messages/welcome_messages/rules/list':          ('GET',            'api'),
    'direct_messages/welcome_messages/rules/show':          ('GET',            'api'),    
    'direct_messages/welcome_messages/rules/destroy':       ('DELETE',         'api'),        

    'favorites/create':                                     ('POST',           'api'),
    'favorites/destroy':                                    ('POST',           'api'),
    'favorites/list':                                       ('GET',            'api'),

    'followers/ids':                                        ('GET',            'api'),
    'followers/list':                                       ('GET',            'api'),

    'friends/ids':                                          ('GET',            'api'),
    'friends/list':                                         ('GET',            'api'),

    'friendships/create':                                   ('POST',           'api'),
    'friendships/destroy':                                  ('POST',           'api'),
    'friendships/incoming':                                 ('GET',            'api'),
    'friendships/lookup':                                   ('GET',            'api'),
    'friendships/no_retweets/ids':                          ('GET',            'api'),
    'friendships/outgoing':                                 ('GET',            'api'),
    'friendships/show':                                     ('GET',            'api'),
    'friendships/update':                                   ('POST',           'api'),

    'lists/create':                                         ('POST',           'api'),
    'lists/destroy':                                        ('POST',           'api'),
    'lists/list':                                           ('GET',            'api'),
    'lists/members':                                        ('GET',            'api'),
    'lists/members/create':                                 ('POST',           'api'),
    'lists/members/create_all':                             ('POST',           'api'),
    'lists/members/destroy':                                ('POST',           'api'),
    'lists/members/destroy_all':                            ('POST',           'api'),
    'lists/members/show':                                   ('GET',            'api'),
    'lists/memberships':                                    ('GET',            'api'),
    'lists/ownerships':                                     ('GET',            'api'),
    'lists/show':                                           ('GET',            'api'),
    'lists/statuses':                                       ('GET',            'api'),
    'lists/subscribers':                                    ('GET',            'api'),
    'lists/subscribers/create':                             ('POST',           'api'),
    'lists/subscribers/destroy':                            ('POST',           'api'),
    'lists/subscribers/show':                               ('GET',            'api'),
    'lists/subscriptions':                                  ('GET',            'api'),
    'lists/update':                                         ('POST',           'api'),

    'media/metadata/create':                                ('POST',           'upload'),
    'media/upload':                                         (['POST','GET'],   'upload'),
    'media/subtitles/create':                               ('POST',           'upload'),
    'media/subtitles/delete':                               ('POST',           'upload'),

    'mutes/users/create':                                   ('POST',           'api'),
    'mutes/users/destroy':                                  ('POST',           'api'),
    'mutes/users/ids':                                      ('GET',            'api'),
    'mutes/users/list':                                     ('GET',            'api'),

    'geo/id/:PARAM':                                        ('GET',            'api'), # PLACE_ID
    'geo/place':                                            ('POST',           'api'),
    'geo/reverse_geocode':                                  ('GET',            'api'),
    'geo/search':                                           ('GET',            'api'),
    'geo/similar_places':                                   ('GET',            'api'),

    'help/configuration':                                   ('GET',            'api'),
    'help/languages':                                       ('GET',            'api'),
    'help/privacy':                                         ('GET',            'api'),
    'help/tos':                                             ('GET',            'api'),

    'saved_searches/create':                                ('POST',           'api'),
    'saved_searches/destroy/:PARAM':                        ('POST',           'api'), # ID
    'saved_searches/list':                                  ('GET',            'api'),
    'saved_searches/show/:PARAM':                           ('GET',            'api'), # ID

    'search/tweets':                                        ('GET',            'api'),

    'statuses/destroy/:PARAM':                              ('POST',           'api'), # ID
    'statuses/home_timeline':                               ('GET',            'api'),
    'statuses/lookup':                                      ('GET',            'api'),
    'statuses/mentions_timeline':                           ('GET',            'api'),
    'statuses/oembed':                                      ('GET',            'api'),
    'statuses/retweet/:PARAM':                              ('POST',           'api'), # ID
    'statuses/retweeters/ids':                              ('GET',            'api'),
    'statuses/retweets/:PARAM':                             ('GET',            'api'), # ID
    'statuses/retweets_of_me':                              ('GET',            'api'),
    'statuses/show/:PARAM':                                 ('GET',            'api'), # ID
    'statuses/unretweet/:PARAM':                            ('POST',           'api'), # ID
    'statuses/user_timeline':                               ('GET',            'api'),
    'statuses/update':                                      ('POST',           'api'),
    'statuses/update_with_media':                           ('POST',           'api'), # deprecated

    'trends/available':                                     ('GET',            'api'),
    'trends/closest':                                       ('GET',            'api'),
    'trends/place':                                         ('GET',            'api'),

    'users/contributees':                                   ('GET',            'api'),
    'users/contributors':                                   ('GET',            'api'),
    'users/lookup':                                         ('POST',           'api'),
    'users/profile_banner':                                 ('GET'             'api'),
    'users/report_spam':                                    ('POST',           'api'),
    'users/search':                                         ('GET',            'api'),
    'users/show':                                           ('GET',            'api'),
    'users/suggestions':                                    ('GET',            'api'),
    'users/suggestions/:PARAM':                             ('GET',            'api'), # SLUG
    'users/suggestions/:PARAM/members':                     ('GET',            'api'), # SLUG

    # COLLECTIONS API

    'collections/create':                                   ('POST',           'api'),
    'collections/destroy':                                  ('POST',           'api'),
    'collections/entries':                                  ('GET',            'api'),
    'collections/entries/add':                              ('POST',           'api'),
    'collections/entries/curate':                           ('POST',           'api'),
    'collections/entries/move':                             ('POST',           'api'),
    'collections/entries/remove':                           ('POST',           'api'),
    'collections/list':                                     ('GET',            'api'),
    'collections/show':                                     ('GET',            'api'),
    'collections/update':                                   ('POST',           'api'),

    # CURATOR API

    'collections/:PARAM/content':                           ('GET',            'curator'), # ID
    'projects':                                             ('GET',            'curator'),
    'projects/:PARAM':                                      ('GET',            'curator'), # ID
    'streams/:PARAM/content':                               ('GET',            'curator'), # ID
    'streams/:PARAM/metrics':                               ('GET',            'curator'), # ID
    'streams/:PARAM/trendline':                             ('GET',            'curator'), # ID
    'streams/compare':                                      ('GET',            'curator'),
    'streams/compare_to_target':                            ('GET',            'curator'),

    # ADS API (not tested!!)

    'accounts/:PARAM/auction_insights':                     ('GET',            'ads-api'), # ACCOUNT ID
    'accounts/:PARAM/promoted_tweets':                      ('GET',            'ads-api'), # ACCOUNT ID
    'stats/accounts/:PARAM':                                ('GET',            'ads-api'), # ACCOUNT ID
    'stats/accounts/:PARAM/reach/funding_instruments':      ('GET',            'ads-api'), # ACCOUNT ID
    'stats/jobs/accounts/:PARAM':                           ('GET',            'ads-api'), # ACCOUNT ID
    'stats/jobs/accounts/:PARAM':                           ('POST',           'ads-api'), # ACCOUNT ID
    'stats/jobs/accounts/:PARAM/:PARAM':                    ('DELETE',         'ads-api'), # ACCOUNT ID, JOB ID
    'stats/jobs/summaries':                                 ('GET',            'ads-api'),
    
    # ACCOUNT ACTIVITY WEBHOOK API

    'account_activity/all/:PARAM/subscriptions':            (['POST', 'DELETE'], 'api'), # ENVIRONMENT NAME
    'account_activity/all/:PARAM/subscriptions/all':        ('GET',              'api'), # ENVIRONMENT NAME
    'account_activity/all/:PARAM/subscriptions/all/list':   ('GET',              'api'), # ENVIRONMENT NAME
    'account_activity/all/:PARAM/subscriptions/list':       ('GET',              'api'), # ENVIRONMENT NAME
    'account_activity/all/:PARAM/webhooks':                 ('POST',             'api'), # ENVIRONMENT NAME    
    'account_activity/all/:PARAM/webhooks/:PARAM':          ('DELETE',           'api'), # ENVIRONMENT NAME, WEBHOOK ID
    'account_activity/all/count':                           ('GET',              'api'), 
    'account_activity/all/webhooks':                        ('GET',              'api'),   
    'account_activity/webhooks':                            ('POST',             'api'),    
    'account_activity/webhooks/:PARAM':                     ('DELETE',           'api'), # WEBHOOK ID
    'account_activity/webhooks/:PARAM/subscriptions':       ('POST',             'api'), # ENVIRONMENT NAME   
    'account_activity/webhooks/:PARAM/subscriptions/list':  ('GET',              'api'), # ENVIRONMENT NAME

    # PREMIUM SEARCH API

    'tweets/search/30day/:PARAM':                           ('GET',              'api'), # LABEL
    'tweets/search/30day/:PARAM/counts':                    ('GET',              'api'), # LABEL
    'tweets/search/fullarchive/:PARAM':                     ('GET',              'api'), # LABEL
    'tweets/search/fullarchive/:PARAM/counts':              ('GET',              'api'), # LABEL
    
    # LABS API (BETAS) WILL NEED APPLICATION APPROVAL

    'labs/1/tweets/metrics/private':                        ('GET',              'api'),
    'labs/2/tweets/:PARAM':                                 ('GET',              'api'), # TWEET ID
    'labs/2/tweets':                                        ('GET',              'api'),
    'labs/2/tweets/search':                                 ('GET',              'api'),
    'labs/2/tweets/:PARAM/hidden':                          ('PUT',              'api'), # TWEET ID
    'labs/2/users/:PARAM':                                  ('GET',              'api'), # USER ID
    'labs/2/users':                                         ('GET',              'api'),          
    
    # !!!!!!!!!!!!!!!!!!!
    # API V2 EARLY ACCESS
    # !!!!!!!!!!!!!!!!!!!

    'compliance/jobs':                                      (['GET','POST'],         'api'), 
    'compliance/jobs/:PARAM':                               ('GET',                  'api'), # ID

    'lists':                                                ('POST',                 'api'),
    'lists/:PARAM':                                         (['GET','PUT','DELETE'], 'api'), # ID
    'lists/:PARAM/followers':                               ('GET',                  'api'),
    'lists/:PARAM/members':                                 (['GET','POST'],         'api'), # ID
    'lists/:PARAM/members/:PARAM':                          ('DELETE',               'api'), # ID, USER ID
    'lists/:PARAM/tweets':                                  ('GET',                  'api'), # ID

    'spaces':                                               ('GET',                  'api'),
    'spaces/:PARAM':                                        ('GET',                  'api'), # ID
    'spaces/:PARAM/buyers':                                 ('GET',                  'api'), # ID
    'spaces/by/creator_ids':                                ('GET',                  'api'),
    'spaces/search':                                        ('GET',                  'api'),

    'tweets':                                               (['GET','POST'],         'api'),
    'tweets/:PARAM':                                        (['GET','DELETE'],       'api'), # ID
    'tweets/:PARAM/hidden':                                 ('PUT',                  'api'), # ID
    'tweets/:PARAM/liking_users':                           ('GET',                  'api'), # ID
    'tweets/:PARAM/retweeted_by':                           ('GET',                  'api'), # ID
    'tweets/counts/all':                                    ('GET',                  'api'),
    'tweets/counts/recent':                                 ('GET',                  'api'),
    'tweets/sample/stream':                                 ('GET',                  'api'),
    'tweets/search/all':                                    ('GET',                  'api'),
    'tweets/search/recent':                                 ('GET',                  'api'),
    'tweets/search/stream':                                 ('GET',                  'api'),
    'tweets/search/stream/rules':                           (['POST','GET'],         'api'), 

    'users':                                                ('GET',                  'api'),
    'users/:PARAM':                                         ('GET',                  'api'), # ID
    'users/:PARAM/blocking':                                (['GET','POST'],         'api'), # ID
    'users/:PARAM/followed_lists':                          (['GET','POST'],         'api'), # ID
    'users/:PARAM/followed_lists/:PARAM':                   ('DELETE',               'api'), # ID, LIST ID
    'users/:PARAM/followers':                               ('GET',                  'api'), # ID
    'users/:PARAM/following':                               (['GET','POST'],         'api'), # ID
    'users/:PARAM/following/:PARAM':                        ('DELETE',               'api'), # USER SOURCE ID, USER TARGET ID
    'users/:PARAM/liked_tweets':                            ('GET',                  'api'), # ID
    'users/:PARAM/likes':                                   ('POST',                 'api'), # ID
    'users/:PARAM/likes/:PARAM':                            ('DELETE',               'api'), # USER ID, TWEET ID
    'users/:PARAM/liked_tweets':                            ('GET',                  'api'), # ID
    'users/:PARAM/list_memberships':                        ('GET',                  'api'), # ID
    'users/:PARAM/mentions':                                ('GET',                  'api'), # ID
    'users/:PARAM/muting':                                  ('GET',                  'api'), # ID
    'users/:PARAM/owned_lists':                             ('GET',                  'api'), # ID
    'users/:PARAM/pinned_lists':                            (['GET','POST'],         'api'), # ID
    'users/:PARAM/pinned_lists/:PARAM':                     ('DELETE',               'api'), # ID, LIST ID
    'users/:PARAM/retweets':                                ('POST',                 'api'), # ID
    'users/:PARAM/retweets/:PARAM':                         ('DELETE',               'api'), # ID, SOURCE TWEET ID
    'users/:PARAM/tweets':                                  ('GET',                  'api'), # ID
    'users/:PARAM/blocking/:PARAM':                         ('DELETE',               'api'), # SOURCE USER ID, TARGET USER ID
    'users/:PARAM/following/:PARAM':                        ('DELETE',               'api'), # SOURCE USER ID, TARGET USER ID
    'users/:PARAM/muting/:PARAM':                           ('DELETE',               'api'), # SOURCE USER ID, TARGET USER ID
    'users/by':                                             ('GET',                  'api'),
    'users/by/username/:PARAM':                             ('GET',                  'api'), # USERNAME
}
