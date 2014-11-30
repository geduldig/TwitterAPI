from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterError
import time
import logging


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

interval = 5

while True:
	logging.info('NEW REQUEST')
	r = api.request('statuses/sample')
	total_count = 0
	total_start = time.time()
	count = 0
	start = total_start
	try:
		for item in r:
			if 'text' in item:
				count += 1
				total_count += 1
				#print(item['text'])
			now = time.time()
			elapsed = now-start
			if elapsed >= interval:
				print('%d\t%d\t%d' % (int(count/elapsed), 
			                      	total_count,
			                      	int(total_count/(now-total_start))))
				start = now
				count = 0
	except TwitterError.TwitterConnectionError as e:
		logging.info(type(e))
		pass
	except KeyboardInterrupt:
		print('user terminated')
		break
	except Exception as e:
		print(type(e))
		print(e)
		break
