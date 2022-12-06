from TwitterAPI import (TwitterAPI, 
                        TwitterOAuth, 
                        TwitterRequestError, 
                        TwitterConnectionError, 
                        HydrateType)


RULES = ['pizza','lambrusco']

EXPANSIONS   = 'author_id'
USER_FIELDS  = 'created_at,description,location,name,username'
TWEET_FIELDS = 'author_id,created_at,entities,id,lang,public_metrics,source,text'


##
## SET UP LOGGING TO FILE AND TO CONSOLE
##

import logging
formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s', '%m/%d/%Y %I:%M:%S %p')
fh = logging.FileHandler('stream_forever.log')
sh = logging.StreamHandler()
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(sh)


##
## AUTHENTICATE WITH TWITTER 
##

o = TwitterOAuth.read_file()
api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')


##
## STREAMING RULES 
##

# ADD RULES (NO HARM RE-ADDING, BUT ONCE IS ENOUGH)
for rule in RULES:
    r = api.request('tweets/search/stream/rules', {'add': [{'value':rule}]})
    print(f'[{r.status_code}] RULE ADDED: {r.text}')
    if r.status_code != 201: exit()

# PRINT RULES
r = api.request('tweets/search/stream/rules', method_override='GET')
print(f'\n[{r.status_code}] RULES:')
if r.status_code != 200: exit()
for item in r:
    print(item['value'])


##
## "BACK OFF" STRATEGY FOR DISCONNECTS AND RATE LIMITS
## USE 60 SECOND INTERVAL FOR HTTP 429 ERRORS
## USE 5 SECOND INTERVAL FOR ALL OTHER HTTP ERRORS
## REFER TO: https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/handling-disconnections
##

from time import sleep

backOffCount = 0

def backOff(interval):
    global backOffCount, logger
    seconds = pow(2, backOffCount) * interval
    backOffCount = min(backOffCount + 1, 6)
    logger.info(f'Back off {seconds} seconds')
    sleep(seconds)


##
## STREAM FOREVER...
##

while True:
    try:
        # START STREAM
        logger.info('START STREAM...')
        r = api.request('tweets/search/stream', 
            {
                'expansions': EXPANSIONS, 
                'user.fields': USER_FIELDS,
                'tweet.fields': TWEET_FIELDS 
            },
            hydrate_type=HydrateType.APPEND)

        if r.status_code == 200:
            logger.info(f'[{r.status_code}] STREAM CONNECTED')
            backOffCount = 0
        else:
            logger.info(f'[{r.status_code}] FAILED TO CONNECT. REASON:\n{r.text}')
            backOff(60 if r.status_code == 429 else 5)            
            continue

        for item in r:
            if 'data' in item:
                print(item['data']['text'])
            elif 'errors' in item:
                logger.error(item['errors'])
            else:
                # PROBABLY SHOULD NEVER BRANCH TO HERE
                logger.warning(f'UNKNOWN ITEM TYPE: {item}')

    except TwitterConnectionError:
        backOff(5)            
        continue

    except TwitterRequestError:
        break

    except KeyboardInterrupt:
        break

    finally:
        logger.info('STREAM STOPPED')