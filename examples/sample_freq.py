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


class Frequency:
	def __init__(self):
		self.interval = 5 # seconds
		self.total_count = 0
		self.total_start = time.time()
		self.interval_count = 0
		self.interval_start = self.total_start

	def record(self):
		self.interval_count += 1
		self.total_count += 1
		now = time.time()
		elapsed = now - self.interval_start
		if elapsed >= self.interval:
			print('%d\t%d\t%d' % (int(self.interval_count/elapsed), 
			                      self.total_count,
			                      int(self.total_count/(now-self.total_start))))
			self.interval_start = now
			self.interval_count = 0


freq = Frequency()


while True:
	try:
		r = api.request('statuses/sample')
		for item in r:
			if 'text' in item:
				freq.record()
			elif 'limit' in item:
				logging.info('TWEETS SKIPPED: %s' % item['limit']['track'])
			elif 'warning' in item:
				logging.info('WARNING: %s' % item['warning'])
			elif 'disconnect' in item:
				# dev.twitter.com/streaming/overview/messages-types#disconnect_messages
				if item['disconnect']['code'] in [2,5,6,7]:
					raise Exception(item['disconnect'])
				else:
					logging.info('RE-CONNECTING: %s' % item['disconnect'])
					break
	except TwitterError.TwitterConnectionError as e:
		logging.info('RE-CONNECTING: %s' % type(e))
		continue
	except KeyboardInterrupt:
		print('TERMINATED BY USER')
		break
	except Exception as e:
		print('TERMINATING: %s %s' % (type(e), e.message))
		break
