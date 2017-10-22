__author__ = "geduldig"
__date__ = "June 7, 2013"
__license__ = "MIT"


from .BearerAuth import BearerAuth as OAuth2
from .constants import *
from datetime import datetime
from requests.exceptions import ConnectionError, ReadTimeout, SSLError
from requests.packages.urllib3.exceptions import ReadTimeoutError, ProtocolError
from requests_oauthlib import OAuth1
from .TwitterError import *
import json
import requests
import socket
import ssl
import time


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
        if auth_type == 'oAuth1':
            if not all([consumer_key, consumer_secret, access_token_key, access_token_secret]):
                raise Exception('Missing authentication parameter')
            self.auth = OAuth1(
                consumer_key,
                consumer_secret,
                access_token_key,
                access_token_secret)
        elif auth_type == 'oAuth2':
            if not all([consumer_key, consumer_secret]):
                raise Exception('Missing authentication parameter')
            self.auth = OAuth2(
                consumer_key,
                consumer_secret,
                proxies=self.proxies)
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
        else:
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

    def request(self, resource, params=None, files=None, method_override=None):
        """Request a Twitter REST API or Streaming API resource.

        :param resource: A valid Twitter endpoint (ex. "search/tweets")
        :param params: Dictionary with endpoint parameters or None (default)
        :param files: Dictionary with multipart-encoded file or None (default)
        :param method_override: Request method to override or None (default)

        :returns: TwitterResponse
        :raises: TwitterConnectionError
        """
        resource, endpoint = self._get_endpoint(resource)
        if endpoint not in ENDPOINTS:
            raise Exception('Endpoint "%s" unsupported' % endpoint)
        with requests.Session() as session:
            session.auth = self.auth
            session.headers = {'User-Agent': USER_AGENT}
            method, subdomain = ENDPOINTS[endpoint]
            if method_override:
                method = method_override
            url = self._prepare_url(subdomain, resource)
            if 'stream' in subdomain:
                session.stream = True
                timeout = STREAMING_TIMEOUT
                # always use 'delimited' for efficient stream parsing
                if not params:
                    params = {}
                params['delimited'] = 'length'
                params['stall_warning'] = 'true'
            else:
                session.stream = False
                timeout = REST_TIMEOUT
            if method == 'POST':
                data = params
                params = None
            else:
                data = None
            try:
                r = session.request(
                    method,
                    url,
                    data=data,
                    params=params,
                    timeout=(CONNECTION_TIMEOUT,timeout),
                    files=files,
                    proxies=self.proxies)
            except (ConnectionError, ProtocolError, ReadTimeout, ReadTimeoutError,
                    SSLError, ssl.SSLError, socket.error) as e:
                raise TwitterConnectionError(e)
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
            raise TwitterRequestError(self.response.status_code)

        if self.stream:
            return iter(_StreamingIterable(self.response))
        else:
            return iter(_RestIterable(self.response))

    def __iter__(self):
        """Get API dependent iterator.

        :returns: Iterator for tweets or other message objects in response.
        :raises: TwitterConnectionError, TwitterRequestError
        """
        return self.get_iterator()

    def get_rest_quota(self):
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
    """

    def __init__(self, response):
        resp = response.json()
        # convert json response into something iterable
        if 'errors' in resp:
            self.results = resp['errors']
        elif 'statuses' in resp:
            self.results = resp['statuses']
        elif 'users' in resp:
            self.results = resp['users']
        elif 'ids' in resp:
            self.results = resp['ids']
        elif 'data' in resp and not isinstance(resp['data'], dict):
            self.results = resp['data']
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
                        elif time.time() - stall_timer > STREAMING_TIMEOUT:
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
                yield item
            except (ConnectionError, ProtocolError, ReadTimeout, ReadTimeoutError,
                    SSLError, ssl.SSLError, socket.error) as e:
                raise TwitterConnectionError(e)
            except AttributeError:
                # inform iterator to exit when client closes connection
                raise StopIteration

    def __iter__(self):
        """Iterator.

        :returns: Tweet status as a JSON object.
        :raises: TwitterConnectionError
        """
        for item in self._iter_stream():
            if item:
                try:
                    yield json.loads(item.decode('utf8'))
                except ValueError as e:
                    # invalid JSON string (possibly an unformatted error message)
                    raise TwitterConnectionError(e)
