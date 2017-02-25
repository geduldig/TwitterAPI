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

USER_AGENT = 'python-TwitterAPI'

CONNECTION_TIMEOUT = 5
STREAMING_TIMEOUT = 90
REST_TIMEOUT = 5

ENDPOINTS = {
    # resource:                                (method, subdomain)

    # STREAMING API

    'statuses/filter':                         ('POST', 'stream'),
    'statuses/firehose':                       ('GET',  'stream'),
    'statuses/sample':                         ('GET',  'stream'),
    'site':                                    ('GET',  'sitestream'),
    'user':                                    ('GET',  'userstream'),

    # PUBLIC API

    'account/remove_profile_banner':           ('POST', 'api'),
    'account/settings':                        ('GET',  'api'),
    'account/update_delivery_device':          ('POST', 'api'),
    'account/update_profile':                  ('POST', 'api'),
    'account/update_profile_background_image': ('POST', 'api'),
    'account/update_profile_banner':           ('POST', 'api'),
    'account/update_profile_colors':           ('POST', 'api'),
    'account/update_profile_image':            ('POST', 'api'),
    'account/verify_credentials':              ('GET',  'api'),

    'application/rate_limit_status':           ('GET',  'api'),

    'blocks/create':                           ('POST', 'api'),
    'blocks/destroy':                          ('POST', 'api'),
    'blocks/ids':                              ('GET',  'api'),
    'blocks/list':                             ('GET',  'api'),

    'direct_messages':                         ('GET',  'api'),
    'direct_messages/destroy':                 ('POST', 'api'),
    'direct_messages/new':                     ('POST', 'api'),
    'direct_messages/sent':                    ('GET',  'api'),
    'direct_messages/show':                    ('GET',  'api'),

    'favorites/create':                        ('POST', 'api'),
    'favorites/destroy':                       ('POST', 'api'),
    'favorites/list':                          ('GET',  'api'),

    'followers/ids':                           ('GET',  'api'),
    'followers/list':                          ('GET',  'api'),

    'friends/ids':                             ('GET',  'api'),
    'friends/list':                            ('GET',  'api'),

    'friendships/create':                      ('POST', 'api'),
    'friendships/destroy':                     ('POST', 'api'),
    'friendships/incoming':                    ('GET',  'api'),
    'friendships/lookup':                      ('GET',  'api'),
    'friendships/no_retweets/ids':             ('GET',  'api'),
    'friendships/outgoing':                    ('GET',  'api'),
    'friendships/show':                        ('GET',  'api'),
    'friendships/update':                      ('POST', 'api'),

    'lists/create':                            ('POST', 'api'),
    'lists/destroy':                           ('POST', 'api'),
    'lists/list':                              ('GET',  'api'),
    'lists/members':                           ('GET',  'api'),
    'lists/members/create':                    ('POST', 'api'),
    'lists/members/create_all':                ('POST', 'api'),
    'lists/members/destroy':                   ('POST', 'api'),
    'lists/members/destroy_all':               ('POST', 'api'),
    'lists/members/show':                      ('GET',  'api'),
    'lists/memberships':                       ('GET',  'api'),
    'lists/ownerships':                        ('GET',  'api'),
    'lists/show':                              ('GET',  'api'),
    'lists/statuses':                          ('GET',  'api'),
    'lists/subscribers':                       ('GET',  'api'),
    'lists/subscribers/create':                ('POST', 'api'),
    'lists/subscribers/destroy':               ('POST', 'api'),
    'lists/subscribers/show':                  ('GET',  'api'),
    'lists/subscriptions':                     ('GET',  'api'),
    'lists/update':                            ('POST', 'api'),

    'media/upload':                            ('POST', 'upload'),

    'mutes/users/create':                      ('POST', 'api'),
    'mutes/users/destroy':                     ('POST', 'api'),
    'mutes/users/ids':                         ('GET',  'api'),
    'mutes/users/list':                        ('GET',  'api'),

    'geo/id/:PARAM':                           ('GET',  'api'), # PLACE_ID
    'geo/place':                               ('POST', 'api'),
    'geo/reverse_geocode':                     ('GET',  'api'),
    'geo/search':                              ('GET',  'api'),
    'geo/similar_places':                      ('GET',  'api'),

    'help/configuration':                      ('GET',  'api'),
    'help/languages':                          ('GET',  'api'),
    'help/privacy':                            ('GET',  'api'),
    'help/tos':                                ('GET',  'api'),

    'saved_searches/create':                   ('POST', 'api'),
    'saved_searches/destroy/:PARAM':           ('POST', 'api'), # ID
    'saved_searches/list':                     ('GET',  'api'),
    'saved_searches/show/:PARAM':              ('GET',  'api'), # ID

    'search/tweets':                           ('GET',  'api'),

    'statuses/destroy/:PARAM':                 ('POST', 'api'), # ID
    'statuses/home_timeline':                  ('GET',  'api'),
    'statuses/lookup':                         ('GET',  'api'),
    'statuses/mentions_timeline':              ('GET',  'api'),
    'statuses/oembed':                         ('GET',  'api'),
    'statuses/retweet/:PARAM':                 ('POST', 'api'), # ID
    'statuses/retweeters/ids':                 ('GET',  'api'),
    'statuses/retweets/:PARAM':                ('GET',  'api'), # ID
    'statuses/retweets_of_me':                 ('GET',  'api'),
    'statuses/show/:PARAM':                    ('GET',  'api'), # ID
    'statuses/unretweet/:PARAM':               ('POST', 'api'), # ID
    'statuses/user_timeline':                  ('GET',  'api'),
    'statuses/update':                         ('POST', 'api'), # deprecated
    'statuses/update_with_media':              ('POST', 'api'),

    'trends/available':                        ('GET',  'api'),
    'trends/closest':                          ('GET',  'api'),
    'trends/place':                            ('GET',  'api'),

    'users/contributees':                      ('GET',  'api'),
    'users/contributors':                      ('GET',  'api'),
    'users/lookup':                            ('POST', 'api'),
    'users/profile_banner':                    ('GET'   'api'),
    'users/report_spam':                       ('POST', 'api'),
    'users/search':                            ('GET',  'api'),
    'users/show':                              ('GET',  'api'),
    'users/suggestions':                       ('GET',  'api'),
    'users/suggestions/:PARAM':                ('GET',  'api'), # SLUG
    'users/suggestions/:PARAM/members':        ('GET',  'api'), # SLUG

    # COLLECTIONS API

    'collections/create':                      ('POST', 'api'),
    'collections/destroy':                     ('POST', 'api'),
    'collections/entries':                     ('GET',  'api'),
    'collections/entries/add':                 ('POST', 'api'),
    'collections/entries/curate':              ('POST', 'api'),
    'collections/entries/move':                ('POST', 'api'),
    'collections/entries/remove':              ('POST', 'api'),
    'collections/list':                        ('GET',  'api'),
    'collections/show':                        ('GET',  'api'),
    'collections/update':                      ('POST', 'api'),

    # CURATOR API

    'collections/:PARAM/content':              ('GET',  'curator'), # ID
    'projects':                                ('GET',  'curator'),
    'projects/:PARAM':                         ('GET',  'curator'), # ID
    'streams/:PARAM/content':                  ('GET',  'curator'), # ID
    'streams/:PARAM/metrics':                  ('GET',  'curator'), # ID
    'streams/:PARAM/trendline':                ('GET',  'curator'), # ID
    'streams/compare':                         ('GET',  'curator'),
    'streams/compare_to_target':               ('GET',  'curator')
}
