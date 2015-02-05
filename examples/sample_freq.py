from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterConnectionError, TwitterRequestError
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

    """Track tweet download statistics"""

    def __init__(self):
        self.interval = 5  # seconds
        self.total_count = 0
        self.total_start = time.time()
        self.interval_count = 0
        self.interval_start = self.total_start

    def update(self):
        self.interval_count += 1
        self.total_count += 1
        now = time.time()
        elapsed = now - self.interval_start
        if elapsed >= self.interval:
            # timestamp : tps : total cumulative tweets : average tps
            print('%s -- %d\t%d\t%d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)),
                                        int(self.interval_count / elapsed),
                                        self.total_count,
                                        int(self.total_count / (now - self.total_start))))
            self.interval_start = now
            self.interval_count = 0


freq = Frequency()


while True:
    try:
        r = api.request('statuses/sample')
        for item in r:
            if 'text' in item:
                freq.update()
            elif 'limit' in item:
                logging.info('TWEETS SKIPPED: %s' % item['limit']['track'])
            elif 'warning' in item:
                logging.warning(item['warning'])
            elif 'disconnect' in item:
                event = item['disconnect']
                if event['code'] in [2,5,6,7]:
                    # streaming connection rejected
                    raise Exception(event)
                logging.info('RE-CONNECTING: %s' % event)
                break
    except TwitterRequestError as e:
        if e.status_code < 500:
            print('REQUEST FAILED: %s' % e)
            break
    except TwitterConnectionError:
        pass
    except KeyboardInterrupt:
        print('TERMINATED BY USER')
        break
    except Exception as e:
        print('STOPPED: %s %s' % (type(e), e))
        break
