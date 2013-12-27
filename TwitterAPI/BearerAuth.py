import requests
import base64
import urllib, urllib2
import json

class BearerAuth(requests.auth.AuthBase):
  def __init__(self, token_url, consumer_key, consumer_secret):
    self._token_url = token_url
    self._consumer_key = consumer_key
    self._consumer_secret = consumer_secret
    self._bearer_token = self.GetAccessToken()

  def GetAccessToken(self):
    b64_bearer_token_creds = base64.b64encode(self._consumer_key + ':' + self._consumer_secret)
    header = {}
    values = {}
    header['User-Agent'] = 'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'
    header['Authorization'] = 'Basic ' + b64_bearer_token_creds
    header['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
    # header['Accept-Encoding'] = 'gzip'
    values['grant_type'] = 'client_credentials'

    data = urllib.urlencode(values)
    req = urllib2.Request(self._token_url, data, header)
    try:
      response = urllib2.urlopen(req)
      data = json.loads(response.read())
      return data['access_token']
    except urllib2.HTTPError:
      # print >> sys.stderr, 'Error while requesting bearer access token: %s' % e
      raise Exception('Twitter error in retrieving bearer access token')

  def __call__(self, r):
    auth_list = [self._consumer_key, self._consumer_secret, self._bearer_token]
    if all(auth_list):
      r.headers['Authorization'] = "Bearer %s" % self._bearer_token
      return r
    else:
      raise Exception('No enough keys passed to Bearer token manager.')