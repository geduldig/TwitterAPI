__author__ = "Jonas Geduldig"
__date__ = "June 7, 2013"
__license__ = "MIT"

from .constants import *
import json
from requests_oauthlib import OAuth1
from .BearerAuth import BearerAuth as OAuth2
from datetime import datetime
import requests


class TwitterAPI(object):

    """Access REST API or Streaming API resources.

    :param consumer_key: Twitter application consumer key
    :param consumer_secret: Twitter application consumer secret
    :param access_token_key: Twitter application access token key
    :param access_token_secret: Twitter application access token secret
    :param auth_type: "oAuth1" (default) or "oAuth2"
    :param proxy_url: HTTPS proxy URL (ex. "https://USER:PASSWORD@SERVER:PORT")
    """

    def __init__(
            self,
            consumer_key=None,
            consumer_secret=None,
            access_token_key=None,
            access_token_secret=None,
            auth_type='oAuth1',
            proxy_url=None):
        """Initialize with your Twitter application credentials"""
        self.proxies = {'https': proxy_url} if proxy_url else None
        if auth_type is 'oAuth1':
            if not all([consumer_key, consumer_secret, access_token_key, access_token_secret]):
                raise Exception('Missing authentication parameter.')
            self.auth = OAuth1(
                consumer_key,
                consumer_secret,
                access_token_key,
                access_token_secret)
        elif auth_type is 'oAuth2':
            if not all([consumer_key, consumer_secret]):
                raise Exception("Missing authentication parameter.")
            self.auth = OAuth2(
                consumer_key,
                consumer_secret,
                proxies=self.proxies)

    def _prepare_url(self, subdomain, path):
        return '%s://%s.%s/%s/%s.json' % (PROTOCOL,
                                          subdomain,
                                          DOMAIN,
                                          VERSION,
                                          path)

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

    def request(self, resource, params=None, files=None, timeout=None):
        """Request a Twitter REST API or Streaming API resource.

        :param resource: A valid Twitter endpoint (ex. "search/tweets")
        :param params: Dictionary with endpoint parameters or None (default)
        :param files: Dictionary with multipart-encoded file or None (default)

        :returns: TwitterAPI.TwitterResponse object
        """
        resource, endpoint = self._get_endpoint(resource)        
        if endpoint not in ENDPOINTS:
            raise Exception('Endpoint "%s" unsupported' % endpoint)
        session = requests.Session()
        session.auth = self.auth
        session.headers = {'User-Agent': USER_AGENT}
        method, subdomain = ENDPOINTS[endpoint]
        url = self._prepare_url(subdomain, resource)
        if 'stream' in subdomain:
            session.stream = True
            if timeout is None:
                timeout = STREAMING_TIMEOUT
            # always use 'delimited' for efficient stream parsing
            if not params:
                params = {}
            params['delimited'] = 'length'
        else:
            session.stream = False
            if timeout is None:
                timeout = REST_TIMEOUT
        if method is 'POST':
            data = params
            params = None
        else:
            data = None
        r = session.request(
            method,
            url,
            data=data,
            params=params,
            timeout=timeout,
            files=files,
            proxies=self.proxies)
        return TwitterResponse(r, session.stream)


class TwitterResponse(object):

    """Response from either a REST API or Streaming API resource call.

    :param response: The requests.Response object returned by the API call
    :param stream: Boolean connection type (True if a streaming connection)
    """

    def __init__(self, response, stream):
        self.response = response
        self.stream = stream

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
        
    def json(self):
        """:returns: response as JSON object."""
        return self.response.json()

    def get_iterator(self):
        """:returns: Iterator for tweets or other message objects in response."""
        if self.stream:
            return iter(_StreamingIterable(self.response))
        else:
            return iter(_RestIterable(self.response))

    def __iter__(self):
        return self.get_iterator()

    def get_rest_quota(self):
        """:returns: Quota information in the REST-only response header."""
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


class _RestIterable(object):

    """Iterate statuses, errors or other iterable objects in a REST API response.

    :param response: The request.Response from a Twitter REST API request
    """

    def __init__(self, response):
        resp = response.json()
        # hack to force json response into something iterable
        if 'errors' in resp:
            self.results = resp['errors']
        elif 'statuses' in resp:
            self.results = resp['statuses']
        elif hasattr(resp, '__iter__') and not isinstance(resp, dict):
            if len(resp) > 0 and 'trends' in resp[0]:
                self.results = resp[0]['trends']
            else:
                self.results = resp
        else:
            self.results = (resp,)

    def __iter__(self):
        """Return a tweet status as a JSON object."""
        for item in self.results:
            yield item


class _StreamingIterable(object):

    """Iterate statuses or other objects in a Streaming API response.

    :param response: The request.Response from a Twitter Streaming API request
    """

    def __init__(self, response):
        self.stream = response.raw
    
    def _iter_stream(self):
        """Return next item in the stream (with or without 'delimited')."""
        while True:
            item = None
            buf = bytearray()
            while True:
                # add bytes until item boundary reached
                buf += self.stream.read(1)
                if buf[-2:] == b'\r\n': 
                    item = buf[0:-2]
                    # when delimited=length, use byte size to read next item
                    if item.isdigit():  
                        item = self.stream.read(int(item))
                    break
            yield item
    
    def __iter__(self):
        """Return a tweet status as a JSON object."""
        for item in self._iter_stream():
            if item:
                try:
                    yield json.loads(item.decode('utf-8'))
                except ValueError:
                    continue


def RestIterator(*args, **kwargs):
    """Deprecated. Use _RestIterable instead."""
    from warnings import warn
    warn('RestIterator is deprecated. Use _RestIterable instead.',
         DeprecationWarning,
         stacklevel=2)
    return _RestIterable(*args, **kwargs)


def StreamingIterator(*args, **kwargs):
    """Deprecated. Use _StreamingIterable instead."""
    from warnings import warn
    warn('StreamingIterator is deprecated. Use _StreamingIterable instead.',
         DeprecationWarning,
         stacklevel=2)
    return _StreamingIterable(*args, **kwargs)

