"""
	All Twitter endpoints.
	
	Version 1.1, Streaming API and REST API.
	
	The complete URL for each endpoint would look like this:
		PROTOCOL://{subdomain}.DOMAIN/VERSION/{resource}?{parameters}
		
	The REST API endpoints all use 'api' for the subdomain.
	The Streaming API endpoints use either POST (with parameters) or GET (without parameters).
"""

__author__ = "Jonas Geduldig"
__date__ = "February 3, 2012"
__license__ = "MIT"


PROTOCOL = 'https'

DOMAIN = 'twitter.com'

VERSION = '1.1'

USER_AGENT = 'python-TwitterAPI.cli.py'

STREAMING_SOCKET_TIMEOUT = 90 # 90 seconds per Twitter's recommendation

STREAMING_ENDPOINTS = {
		# resource:                                ( subdomain )

		'statuses/filter':                         ('stream',),
		'statuses/firehose':                       ('stream',),
		'statuses/sample':                         ('stream',),
		'site':                                    ('sitestream',),
		'user':                                    ('userstream',)
}

REST_SUBDOMAIN = 'api'

REST_SOCKET_TIMEOUT = 5

REST_ENDPOINTS = {
		# resource:                                ( method )

		'statuses/destroy/:PARAM':                 ('POST',), # ID
		'statuses/home_timeline':                  ('GET',),
		'statuses/mentions_timeline':              ('GET',),
		'statuses/oembed':                         ('GET',),
		'statuses/retweets_of_me':                 ('GET',),
		'statuses/retweet/:PARAM':                 ('POST',), # ID
		'statuses/retweets/:PARAM':                ('GET',),  # ID
		'statuses/show/:PARAM':                    ('GET',),  # ID
		'statuses/user_timeline':                  ('GET',),
		'statuses/update':                         ('POST',),
		'statuses/update_with_media':              ('POST',),

		'search/tweets':                           ('GET',),

		'direct_messages':                         ('GET',),
		'direct_messages/destroy':                 ('POST',),
		'direct_messages/new':                     ('POST',),
		'direct_messages/sent':                    ('GET',),
		'direct_messages/show':                    ('GET',),

		'friends/ids':                             ('GET',),
		'friends/list':                            ('GET',),

		'followers/ids':                           ('GET',),
		'followers/list':                          ('GET',),

		'friendships/create':                      ('POST',),
		'friendships/destroy':                     ('POST',),
		'friendships/incoming':                    ('GET',),
		'friendships/lookup':                      ('GET',),
		'friendships/no_retweets/ids':             ('GET',),
		'friendships/outgoing':                    ('GET',),
		'friendships/show':                        ('GET',),
		'friendships/update':                      ('POST',),

		'account/remove_profile_banner':           ('POST',),
		'account/settings':                        ('GET',),
		'account/update_delivery_device':          ('POST',),
		'account/update_profile':                  ('POST',),
		'account/update_profile_background_image': ('POST',),
		'account/update_profile_banner':           ('POST',),
		'account/update_profile_colors':           ('POST',),
		'account/update_profile_image':            ('POST',),
		'account/verify_credentials':              ('GET',),

		'blocks/create':                           ('POST',),
		'blocks/destroy':                          ('POST',),
		'blocks/ids':                              ('GET',),
		'blocks/list':                             ('GET',),

		'users/contributees':                      ('GET',),
		'users/contributors':                      ('GET',),
		'users/lookup':                            ('GET',),
		'users/profile_banner':                    ('get'),
		'users/report_spam':                       ('POST',),
		'users/search':                            ('GET',),
		'users/show':                              ('GET',),
		'users/suggestions':                       ('GET',),
		'users/suggestions/:PARAM':                ('GET',),  # SLUG
		'users/suggestions/:PARAM/members':        ('GET',),  # SLUG

		'favorites/create':                        ('POST',),
		'favorites/destroy':                       ('POST',),
		'favorites/list':                          ('GET',),

		'lists/create':                            ('POST',),
		'lists/destroy':                           ('POST',),
		'lists/list':                              ('GET',),
		'lists/members':                           ('GET',),
		'lists/members/create':                    ('POST',),
		'lists/members/create_all':                ('POST',),
		'lists/members/destroy':                   ('POST',),
		'lists/members/destroy_all':               ('POST',),
		'lists/members/show':                      ('GET',),
		'lists/memberships':                       ('GET',),
		'lists/show':                              ('GET',),
		'lists/statuses':                          ('GET',),
		'lists/subscribers':                       ('GET',),
		'lists/subscribers/create':                ('POST',),
		'lists/subscribers/destroy':               ('POST',),
		'lists/subscribers/show':                  ('GET',),
		'lists/subscriptions':                     ('GET',),
		'lists/update':                            ('POST',),

		'saved_searches/create':                   ('POST',),
		'saved_searches/destroy/:PARAM':           ('POST',), # ID
		'saved_searches/list':                     ('GET',),
		'saved_searches/show/:PARAM':              ('GET',),  # ID

		'geo/id/:PARAM':                           ('GET',),  # PLACE_ID
		'geo/place':                               ('POST',),
		'geo/reverse_geocode':                     ('GET',),
		'geo/search':                              ('GET',),
		'geo/similar_places':                      ('GET',),

		'trends/available':                        ('GET',),
		'trends/closest':                          ('GET',),
		'trends/place':                            ('GET',),

		'oauth/access_token':                      ('POST',),
		'oauth/authenticate':                      ('GET',),
		'oauth/authorize':                         ('GET',),
		'oauth/request_token':                     ('POST',),

		'help/configuration':                      ('GET',),
		'help/languages':                          ('GET',),
		'help/privacy':                            ('GET',),
		'help/tos':                                ('GET',),

		'application/rate_limit_status':           ('GET',)
}
