# The purpose is to learn standard logging to use e.g. in docker (using python 3.8.5)

import logging
import LearnLogging.internal

LOG_FILE_FORMAT = '%(asctime)s MY_PREFIX [%(module)-15.15s] [%(levelname)-6.6s]  %(message)s'
LOG_CONSOLE_FORMAT = '%(module)s - %(message)s'

logging.basicConfig(filename='main.log', level=logging.INFO, format=LOG_FILE_FORMAT)

logging.debug('Debug message sent from the main file')
logging.info('Debug message sent from the main file')
logging.info('So should this')
logging.warning('And this, too')

#logger = logging.getLogger(__name__)
#logger.info("LOGGER - Send using logger before start")

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter(LOG_CONSOLE_FORMAT))

logger = logging.getLogger(__name__)
# add ch to logger
logger.addHandler(ch)
logger.info("Sent using logger after adding StreamHandler. To both stdout and file ")

if __name__ == '__main__':

    logging.info('Sent using LOGGING from the calling main. Appears in the FILE ONLY.')
    a = LearnLogging.internal.internal(logger)
    logger.info("LOGGER - Send using logger INFO in main")
    logger.debug("LOGGER - Send using logger DEBUG in main")
