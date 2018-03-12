from TwitterAPI import TwitterAPI
import logging

# SET UP LOGGING TO FILE AND TO CONSOLE
formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s',
                              '%m/%d/%Y %I:%M:%S %p')
fh = logging.FileHandler('logging.log')
fh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

logging.info('START SAMPLE STREAM')

try:
    r = api.request('statuses/sample')
    for item in r:
        if 'text' in item:
            print(item['text'])
        elif:
            logging.info('NOT A TWEET: %s' % item.text)
except Exception as e:
	logging.warning('STOPPING: %s' % str(e))