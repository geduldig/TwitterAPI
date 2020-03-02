from TwitterAPI import TwitterAPI, TwitterConnectionError, TwitterRequestError
import time

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

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

# THIS DEMONSTRATES HOW TO HANDLE ALL TYPES OF STREAMING ERRORS.
# SO, THIS IS APPLICAPLE TO 'statuses/filter' AS WELL. ONLY WHEN
# APPROPRIATE, A DROPPED CONNECTION IS RE-ESTABLISHED. 

while True:
    try:
        r = api.request('statuses/sample')
        for item in r:
            if 'text' in item:
                freq.update()
            elif 'limit' in item:
                print('TWEETS SKIPPED: %s' % item['limit']['track'])
            elif 'warning' in item:
                print(item['warning'])
            elif 'disconnect' in item:
                event = item['disconnect']
                if event['code'] in [2,5,6,7]:
                    # streaming connection rejected
                    raise Exception(event)
                print('RE-CONNECTING: %s' % event)
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