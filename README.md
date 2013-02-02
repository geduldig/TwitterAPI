### UNDER DEVELOPMENT ###

_Expected release date is sometime in early February 2013_

---

# twitterapi #

_Python classes and command line scripts for using the Twitter API._

### What's it do? ###

This python package can download tweets, post tweets and get tweet trends.  You can either use the classes to program your own requests to twitter.com, or you can use the command line scripts in the twitterapi.tools sub-module.

The classes implement the following Twitter Streaming API and REST API endpoints:

* statuses/filter (Streaming API, version 1.1)
* search/tweets (REST API, version 1.1)
* statuses/update (REST API, version 1.1)
* trends/place and trends/places (REST API, version 1.1)

If you need other Twitter endpoints, it shouldn't be much trouble to add them.  The design goal is to use a minimal amount of code to provide an easy to use/understand/modify implementation of the Twitter API.

### Features ###

*Retrieving Tweets*

There are two classes, TwSearch and TwStream, that provide methods for downloading tweets.  Use TwSearch to search old or new tweets; use TwStream to stream current tweets in real-time.  In either case, the tweets are returned as dictionaries containing the entire status record, which include the tweet text, user info and much more. 

In addition to tweets (i.e. status messages), sometimes Twitter sends other types of useful messages.  For example, TwStream may return a rate limit message which contains the total number of tweets skipped due to bandwidth restrictions. 

TwSearch has a few convenience methods:

* TwSearch.get_quota() returns the quota status, including the remaining number of searches and, if the quota was exceeded, the time until which searches should be suspended.

* TwSearch.past_results() returns tweets by successively calling TwSearch.results().  With each call the previous 'page' of tweets is returned.  However, this is hidden so that all the client sees is a generator successively older tweets.  Twitter will return at most about 1 week of old tweets unless the generator quits with a quota exceeded exception first.

* TwSearch.new_results() operates similarly to past_results() except pages of newer rather than older tweets are returned.  Like the streaming method, this method is not guaranteed to get all tweets.  TwStream.results() and TwSearch.new_results() return mostly the same tweets, although you will see discrepancies. 

*Posting Tweets*

TwUpdate provides a method for posting (tweeting) a 140 character message.

*Trends*

TwTrends has a method for getting the trending words and hashtags for a given place, and another method for getting all places (countries and towns) that have trending data.  For added convenience, there is also a method for returning worldwide trends.

### Authentication ###

Twitter requests require OAuth authentication.  This is done by passing an instance of TwCredentials to the initiator of any class.  TwCredentials is a simple class for holding OAuth's consumer and access token keys and secrets.  You can either instantiate TwCredentials class with the four keys and secrets, or use the the TwCredentials class method read_file which reads a text file that has a line for each key and secret, like this:

`consumer_key=<YOUR CONSUMER KEY>'
`consumer_secret=<YOUR CONSUMER SECRET>'
`access_token_key=<YOUR ACCESS TOKEN KEY>'
`access_token_secret=<YOUR ACCESS TOKEN SECRET>'

### Extras ###

Sub-package twitterapi.tools has command line scripts that demonstrate how to work with the classes.  You will first need to enter your twitter application credentials in twitterapi/tools/credentials.txt.  Then, you can use the following syntax:

`python -m twitterapi.tools.Search [-new] word(s)`
`python -m twitterapi.tools.Stream word(s)`
`python -m twitterapi.tools.Trends [-woeid woeid]`
`python -m twitterapi.tools.Update message`

### External Dependencies ###

This package uses the following external package.

* oauth2 - for authentication with Twitter

### Installation ###

I like to use pip: 
`pip install puttytat`

Before running scripts in the twitterapi.test and twitterapi.tools sub-pacages, you must add your Twitter OAuth application credentials in twitterapi/test/credentials.txt and in twitterapi/tools/credentials.txt.  If you do not have credentials, first create a Twitter application by logging into dev.twitter.com.  Run scripts with the -m option.  For example,

`python -m twitterapi.test.test_search`

### Contributors ###

Jonas Geduldig
