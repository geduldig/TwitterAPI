__author__ = "geduldig"
__date__ = "June 8, 2013"
__license__ = "MIT"


from .TwitterAPI import HydrateType
from .TwitterError import *
from requests.exceptions import ConnectionError, ReadTimeout, SSLError
from requests.packages.urllib3.exceptions import ReadTimeoutError, ProtocolError
import requests
import time


class TwitterPager(object):

    """Continuous (stream-like) pagination of response from Twitter REST API resource.
    In addition to Public API endpoints, supports Premium Search API.

    :param api: An authenticated TwitterAPI object
    :param resource: String with the resource path (ex. search/tweets)
    :param params: Dictionary of resource parameters
    :param hydrate_type: HydrateType or int
                         Do not hydrate - NONE or 0 (default)
                         Append new field with '_hydrate' suffix with hydrate values - APPEND or 1
                         Replace current field value with hydrate values - REPLACE or 2
    """

    def __init__(self, api, resource, params=None, hydrate_type=HydrateType.NONE):
        self.api = api
        self.resource = resource
        if not params:
            params = {}
        self.params = params
        self.hydrate_type = hydrate_type

    def get_iterator(self, wait=5, new_tweets=False):
        """Iterate response from Twitter REST API resource. Resource is called
        in a loop to retrieve consecutive pages of results.

        :param wait: Floating point number (default=5) of seconds wait between requests.
                     Depending on the resource, appropriate values are 5 or 60 seconds.
        :param new_tweets: Boolean determining the search direction.
                           False (default) retrieves old results.
                           True retrieves current results.

        :returns: JSON objects containing statuses, errors or other return info.
        """
        elapsed = 0
        while True:
            try:
                # REQUEST ONE PAGE OF RESULTS...
                start = time.time()
                r = self.api.request(self.resource, self.params, hydrate_type=self.hydrate_type)
                it = r.get_iterator()
                if new_tweets:
                    it = reversed(list(it))

                # YIELD FOR EACH ITEM IN THE PAGE...
                item_count = 0
                id = None
                for item in it:
                    item_count += 1
                    if type(item) is dict:
                        if 'id' in item:
                            id = item['id']
                        if 'code' in item:
                            if item['code'] in [130, 131]:
                                # Twitter service error
                                raise TwitterConnectionError(item)
                    yield item

                data = r.json()

                # CHECK FOR NEXT PAGE OR BAIL...
                if self.api.version == '1.1':
                    # if a cursor is present, use it to get next page
                    # otherwise, use id to get next page
                    is_premium_search = self.params and 'query' in self.params and self.api.version == '1.1'
                    cursor = -1
                    if new_tweets and 'previous_cursor' in data:
                        cursor = data['previous_cursor']
                        cursor_param = 'cursor'
                    elif not new_tweets:
                        if 'next_cursor' in data:
                            cursor = data['next_cursor']
                            cursor_param = 'cursor'
                        elif 'next' in data:
                            # 'next' is used by Premium Search (OLD searches only)
                            cursor = data['next']
                            cursor_param = 'next'

                    # bail when no more results
                    if cursor == 0:
                        break
                    elif cursor == -1 and is_premium_search:
                        break
                    elif not new_tweets and item_count == 0:
                        break
                else: # VERSION 2
                    meta = data['meta']
                    if not new_tweets and not 'next_token' in meta:
                        break

                # SLEEP...
                elapsed = time.time() - start
                pause = wait - elapsed if elapsed < wait else 0
                time.sleep(pause)

                # SETUP REQUEST FOR NEXT PAGE...
                if self.api.version == '1.1':
                    # get a page with cursor if present, or with id if not
                    # a Premium search (i.e. 'query' is not a parameter)
                    if cursor != -1:
                        self.params[cursor_param] = cursor
                    elif id is not None and not is_premium_search:
                        if new_tweets:
                            self.params['since_id'] = str(id)
                        else:
                            self.params['max_id'] = str(id - 1)
                    else:
                        continue
                else: # VERSION 2
                    # TWITTER SHOULD STANDARDIZE ON pagination_token IN THE FUTURE
                    SEARCH_ENDPOINTS = ['tweets/search/recent', 'tweets/search/all']
                    pagination_token = 'next_token' if self.resource in SEARCH_ENDPOINTS else 'pagination_token'
                    if new_tweets:
                        self.params[pagination_token] = meta['previous_token']
                    else:
                        self.params[pagination_token] = meta['next_token']

            except TwitterRequestError as e:
                if e.status_code < 500:
                    raise
                continue
            except TwitterConnectionError:
                continue