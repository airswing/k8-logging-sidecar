import logging
import time

logging.warning('App test starting up...')
logging.warning('Start up completed! Test daemon running.')

while True:
    time.sleep(5)
    logging.warning('App test event occured at: ' + time.ctime())
