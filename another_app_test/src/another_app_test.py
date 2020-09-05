import logging
import time

logging.warning('ANOTHER APP TEST STARTING UP...')
logging.warning('START UP COMPLETED! TEST RUNNING...')

while True:
    time.sleep(2)
    logging.warning('ANOTHER APP TEST EVENT OCCURED AT: ' + time.ctime())
