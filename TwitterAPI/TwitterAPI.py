__author__ = "geduldig"
__date__ = "June 7, 2013"
__license__ = "MIT"


from .BearerAuth import BearerAuth as OAuth2
from .constants import *
from .TwitterError import *
from datetime import datetime
from enum import Enum
from requests.exceptions import ConnectionError, ReadTimeout, SSLError
from requests.packages.urllib3.exceptions import ReadTimeoutError, ProtocolError
from requests_oauthlib import OAuth1
import json
import os
import requests
import socket
import ssl
import time


DEFAULT_USER_AGENT = os.getenv('DEFAULT_USER_AGENT', 'python-TwitterAPI')
DEFAULT_CONNECTION_TIMEOUT = os.getenv('DEFAULT_CONNECTION_TIMEOUT', 5)
DEFAULT_STREAMING_TIMEOUT = os.getenv('DEFAULT_STREAMING_TIMEOUT', 90)
DEFAULT_REST_TIMEOUT = os.getenv('DEFAULT_REST_TIMEOUT', 5)


class OAuthType(Enum):
    OAUTH1 = 'oAuth1'
    OAUTH2 = 'oAuth2'


class HydrateType(Enum):
    NONE = 0
    APPEND = 1
    REPLACE = 2


class TwitterAPI(object):

    """Access REST API or Streaming API resources.

    :param consumer_key: Twitter application consumer key
    :param consumer_secret: Twitter application consumer secret
    :param access_token_key: Twitter application access token key
    :param access_token_secret: Twitter application access token secret
    :param auth_type: "oAuth1" (default) or "oAuth2"
    :param proxy_url: HTTPS proxy URL string (ex. 'https://USER:PASSWORD@SERVER:PORT'),
                      or dict of URLs (ex. {'http':'http://SERVER', 'https':'https://SERVER'})
    """

    # static properties to be overridden if desired
    USER_AGENT = DEFAULT_USER_AGENT
    CONNECTION_TIMEOUT = DEFAULT_CONNECTION_TIMEOUT
    STREAMING_TIMEOUT = DEFAULT_STREAMING_TIMEOUT
    REST_TIMEOUT = DEFAULT_REST_TIMEOUT

    def __init__(
            self,
            consumer_key=None,
            consumer_secret=None,
            access_token_key=None,
            access_token_secret=None,
            auth_type=OAuthType.OAUTH1,
            proxy_url=None,
            api_version=VERSION):
        """Initialize with your Twitter application credentials"""
        # if there are multiple API versions, this will be the default version which can
        # also be overridden by specifying the version when calling the request method.
        self.version = api_version

        # Optional proxy or proxies.
        if isinstance(proxy_url, dict):
            self.proxies = proxy_url
        elif proxy_url is not None:
            self.proxies = {'https': proxy_url}
        else:
            self.proxies = None

        # Twitter supports two types of authentication.
        if auth_type == OAuthType.OAUTH1 or auth_type == 'oAuth1':
            if not all([consumer_key, consumer_secret, access_token_key, access_token_secret]):
                raise Exception('Missing authentication parameter')
            self.auth = OAuth1(
                consumer_key,
                consumer_secret,
                access_token_key,
                access_token_secret)
        elif auth_type == OAuthType.OAUTH2 or auth_type == 'oAuth2':
            if not all([consumer_key, consumer_secret]):
                raise Exception('Missing authentication parameter')
            self.auth = OAuth2(
                consumer_key,
                consumer_secret,
                proxies=self.proxies,
                user_agent=self.USER_AGENT)
        else:
            raise Exception('Unknown oAuth version')

    def _prepare_url(self, subdomain, path):
        if subdomain == 'curator':
            return '%s://%s.%s/%s/%s.json' % (PROTOCOL,
                                              subdomain,
                                              DOMAIN,
                                              CURATOR_VERSION,
                                              path)
        elif subdomain == 'ads-api':
            return '%s://%s.%s/%s/%s'      % (PROTOCOL,
                                              subdomain,
                                              DOMAIN,
                                              ADS_VERSION,
                                              path)
        elif subdomain == 'api' and 'labs/' in path:
            return '%s://%s.%s/%s'         % (PROTOCOL,
                                              subdomain,
                                              DOMAIN,
                                              path)        
        elif self.version == '1.1':
            return '%s://%s.%s/%s/%s.json' % (PROTOCOL,
                                              subdomain,
                                              DOMAIN,
                                              self.version,
                                              path)
        elif self.version == '2':
            return '%s://%s.%s/%s/%s'      % (PROTOCOL,
                                              subdomain,
                                              DOMAIN,
                                              self.version,
                                              path)
        else:
            raise Exception('Unsupported API version')

    def _get_endpoint(self, resource):
        """Substitute any parameters in the resource path with :PARAM."""
        if ':' in resource:
            parts = resource.split('/')
            # embedded parameters start with ':'
            parts = [k if k[0] != ':' else ':PARAM' for k in parts]
            endpoint = '/'.join(parts)
            resource = resource.replace(':', '')
            return (resource, endpoint)
        else:
            return (resource, resource)

    def request(self, resource, params=None, files=None, method_override=None, hydrate_type=HydrateType.NONE):
        """Request a Twitter REST API or Streaming API resource.

        :param resource: A Twitter endpoint (ex. "search/tweets")
        :param params: Dictionary with endpoint parameters or None (default)
        :param files: Dictionary with multipart-encoded file or None (default)
        :param method_override: Request method to override or None (default)
        :param hydrate_type: HydrateType or int
                             Do not hydrate - NONE or 0 (default)
                             Append new field with '_hydrate' suffix with hydrate values - APPEND or 1
                             Replace current field value with hydrate values - REPLACE or 2

        :returns: TwitterResponse
        :raises: TwitterConnectionError
        """
        resource, endpoint = self._get_endpoint(resource)
        if endpoint not in ENDPOINTS:
            raise Exception('Endpoint "%s" unsupported' % endpoint)
        with requests.Session() as session:
            session.auth = self.auth
            session.headers = {'User-Agent': self.USER_AGENT}
            method, subdomain = ENDPOINTS[endpoint]
            if method_override:
                method = method_override
            url = self._prepare_url(subdomain, resource)
            if self.version == '1.1' and 'stream' in subdomain:
                session.stream = True
                timeout = self.STREAMING_TIMEOUT
                # always use 'delimited' for efficient stream parsing
                if not params:
                    params = {}
                params['delimited'] = 'length'
                params['stall_warning'] = 'true'
            elif self.version == '2' and resource.endswith('/stream'):
                session.stream = True
                timeout = self.STREAMING_TIMEOUT
            else:
                session.stream = False
                timeout = self.REST_TIMEOUT
            d = p = j = None
            if method == 'POST':
                if self.version == '1.1':
                    d = params
                else:
                    j = params
            elif method == 'PUT':
                j = params
            else:
                p = params

            try:           
                if False and method == 'PUT':
                    session.headers['Content-type'] = 'application/json'            
                    data = params                        
                    r = session.request(
                        method,
                        url,
                        json=data)                
                else:
                    r = session.request(
                        method,
                        url,
                        data=d,
                        params=p,
                        json=j,
                        timeout=(self.CONNECTION_TIMEOUT, timeout),
                        files=files,
                        proxies=self.proxies)
            except (ConnectionError, ProtocolError, ReadTimeout, ReadTimeoutError,
                    SSLError, ssl.SSLError, socket.error) as e:
                raise TwitterConnectionError(e)

            options = {
                'api_version': self.version,
                'is_stream': session.stream,
                'hydrate_type': hydrate_type
            }
            return TwitterResponse(r, options)


class TwitterResponse(object):

    """Response from either a REST API or Streaming API resource call.

    :param response: The requests.Response object returned by the API call
    :param stream: Boolean connection type (True if a streaming connection)
    :param options: Dict containing parsing options
    """

    def __init__(self, response, options):
        self.response = response
        self.options = options

    @property
    def headers(self):
        """:returns: Dictionary of API response header contents."""
        return self.response.headers

    @property
    def status_code(self):
        """:returns: HTTP response status code."""
        return self.response.status_code

    @property
    def text(self):
        """:returns: Raw API response text."""
        return self.response.text

    def json(self, **kwargs):
        """Get the response as a JSON object.

        :param \*\*kwargs: Optional arguments that ``json.loads`` takes.
        :returns: response as JSON object.
        :raises: ValueError
        """
        return self.response.json(**kwargs)

    def get_iterator(self):
        """Get API dependent iterator.

        :returns: Iterator for tweets or other message objects in response.
        :raises: TwitterConnectionError, TwitterRequestError
        """
        if self.response.status_code != 200:
            raise TwitterRequestError(self.response.status_code, msg=self.response.text)

        if self.options['is_stream']:
            return iter(_StreamingIterable(self.response, self.options))
        else:
            return iter(_RestIterable(self.response, self.options))

    def __iter__(self):
        """Get API dependent iterator.

        :returns: Iterator for tweets or other message objects in response.
        :raises: TwitterConnectionError, TwitterRequestError
        """
        return self.get_iterator()

    def get_quota(self):
        """Quota information in the REST-only response header.

        :returns: Dictionary of 'remaining' (count), 'limit' (count), 'reset' (time)
        """
        remaining, limit, reset = None, None, None
        if self.response:
            if 'x-rate-limit-remaining' in self.response.headers:
                remaining = int(
                    self.response.headers['x-rate-limit-remaining'])
                if remaining == 0:
                    limit = int(self.response.headers['x-rate-limit-limit'])
                    reset = int(self.response.headers['x-rate-limit-reset'])
                    reset = datetime.fromtimestamp(reset)
        return {'remaining': remaining, 'limit': limit, 'reset': reset}

    def close(self):
        """Disconnect stream (blocks with Python 3)."""
        self.response.raw.close()


class _RestIterable(object):

    """Iterate statuses, errors or other iterable objects in a REST API response.

    :param response: The request.Response from a Twitter REST API request
    :param options: Dict containing parsing options
    """

    def __init__(self, response, options):
        resp = response.json()
        if options['api_version'] == '2':
            if 'data' in resp:
                if isinstance(resp['data'], dict):
                    resp['data'] = [resp['data']]
                h_type = options['hydrate_type']
                if 'includes' in resp and h_type != HydrateType.NONE:
                    field_suffix = '' if h_type == HydrateType.REPLACE else '_hydrate'                        
                    self.results = _hydrate_tweets(resp['data'], resp['includes'], field_suffix)
                else:
                    self.results = resp['data']
            else:
                self.results = []
        elif options['api_version'] == '1.1':
            # convert json response into something iterable
            if 'errors' in resp:
                self.results = resp['errors']
            elif 'statuses' in resp:
                self.results = resp['statuses']
            elif 'users' in resp:
                self.results = resp['users']
            elif 'ids' in resp:
                self.results = resp['ids']
            elif 'results' in resp:
                self.results = resp['results']
            elif 'data' in resp:
                if not isinstance(resp['data'], dict):
                    self.results = resp['data']
                else:
                    self.results = [resp['data']]
            elif hasattr(resp, '__iter__') and not isinstance(resp, dict):
                if len(resp) > 0 and 'trends' in resp[0]:
                    self.results = resp[0]['trends']
                else:
                    self.results = resp
            else:
                self.results = (resp,)
        else:
            self.results = []

    def __iter__(self):
        """
        :returns: Tweet status as a JSON object.
        """
        for item in self.results:
            yield item


class _StreamingIterable(object):

    """Iterate statuses or other objects in a Streaming API response.

    :param response: The request.Response from a Twitter Streaming API request
    :param options: Dict containing parsing options
    """

    def __init__(self, response, options):
        self.stream = response.raw
        self.options = options

    def _iter_stream(self):
        """Stream parser.

        :returns: Next item in the stream (may or may not be 'delimited').
        :raises: TwitterConnectionError, StopIteration
        """
        while True:
            item = None
            buf = bytearray()
            stall_timer = None
            try:
                while True:
                    # read bytes until item boundary reached
                    buf += self.stream.read(1)
                    if not buf:
                        # check for stall (i.e. no data for 90 seconds)
                        if not stall_timer:
                            stall_timer = time.time()
                        elif time.time() - stall_timer > TwitterAPI.STREAMING_TIMEOUT:
                            raise TwitterConnectionError('Twitter stream stalled')
                    elif stall_timer:
                        stall_timer = None
                    if buf[-2:] == b'\r\n':
                        item = buf[0:-2]
                        if item.isdigit():
                            # use byte size to read next item
                            nbytes = int(item)
                            item = None
                            item = self.stream.read(nbytes)
                        break
                if item:
                    item = json.loads(item.decode('utf8'))
                    if self.options['api_version'] == '2':
                        h_type = self.options['hydrate_type']
                        if h_type != HydrateType.NONE:
                            if 'data' in item and 'includes' in item:
                                field_suffix = '' if h_type == HydrateType.REPLACE else '_hydrate' 
                                item = { 'data':_hydrate_tweets(item['data'], item['includes'], field_suffix) }
                yield item
            except (ConnectionError, ValueError, ProtocolError, ReadTimeout, ReadTimeoutError,
                    SSLError, ssl.SSLError, socket.error, json.decoder.JSONDecodeError) as e:
                raise TwitterConnectionError(e)
            except AttributeError:
                # inform iterator to exit when client closes connection
                raise StopIteration

    def __iter__(self):
        """
        :returns: Tweet status as a JSON object.
        :raises: TwitterConnectionError
        """
        for item in self._iter_stream():
            if item:
                yield item


def _hydrate_tweets(data, includes, field_suffix):
    """Insert expansion fields back into tweet data by appending
    a new field as a sibling to the referenced field.

    :param data: "data" property value in JSON response
    :param includes: "includes" property value in JSON response
    :param field_suffix: Suffix appended to a hydrated field name.
                         Either "_hydrate" which puts hydrated values into
                         a new field, or "" which replaces the current
                         field value with hydrated values.
                         
    :returns: Tweet status as a JSON object.
    """
    new_fields = []
    for key in includes:
        incl = includes[key]
        for obj in incl:
            for field in ['id', 'media_key', 'username']:
                if field in obj:
                    _create_include_fields(data, (obj[field], obj), new_fields)

    for item in new_fields:
        parent = item[0]
        field = item[1] + field_suffix
        include = item[2]
        parent[field] = include
    return data


def _create_include_fields(parent, include, new_fields):
    """Depth-first seach into 'parent' to locate fields referenced in
    'include'. Each match is appended to 'new_fields'.
    """
    if isinstance(parent, list):
        for item in parent:
            _create_include_fields(item, include, new_fields)
    elif isinstance(parent, dict):
        for key, value in parent.items():
            if value == include[0]:
                new_fields.append((parent, key, include[1]))
            else:
                _create_include_fields(value, include, new_fields)