from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterError
import time
import logging


# SET UP LOGGING TO FILE AND TO CONSOLE
formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s',
                              '%m/%d/%Y %I:%M:%S %p')
fh = logging.FileHandler('sample_freq.log')
fh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)


o = TwitterOAuth.read_file()
api = TwitterAPI(o.consumer_key, 
                 o.consumer_secret, 
                 o.access_token_key, 
                 o.access_token_secret)

interval = 5 # seconds

while True:
	total_count = 0
	total_start = time.time()
	interval_count = 0
	interval_start = total_start
	try:
		r = api.request('statuses/sample')
		for item in r:
			if 'text' in item:
				interval_count += 1
				total_count += 1
			elif 'warning' in item:
				print(item['warning'])
			# PRINT TWEETS PER SECOND
			now = time.time()
			elapsed = now - interval_start
			if elapsed >= interval:
				print('%d\t%d\t%d' % (int(interval_count/elapsed), 
			                      	total_count,
			                      	int(total_count/(now-total_start))))
				interval_start = now
				interval_count = 0
	except TwitterError.TwitterConnectionError as e:
		logging.info('RE-CONNECTING: %s' % type(e))
	except KeyboardInterrupt:
		print('TERMINATED BY USER')
		break
	except Exception as e:
		print('TERMINATING: %s %s' % (type(e), e.message))
		break
