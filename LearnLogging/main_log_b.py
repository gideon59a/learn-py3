# The purpose is to learn standard logging to use e.g. in docker (using python 3.8.5)
import LearnLogging.internal

import logging
#logging.basicConfig(filename='main.log', level=logging.INFO)
#logging.debug(' Message sent from the main file')
#logging.info('So should this')
#logging.warning('And this, too')
#logger = logging.getLogger(__name__)
#logger.info("LOGGER - Send using logger before start")

LOG_FILE_MODE = 'w+'
LOG_LOGFILE_FORMAT = '%(asctime)s [%(module)-15.15s] [%(levelname)-6.6s]  %(message)s'

fh = logging.FileHandler("file.log", mode=LOG_FILE_MODE)
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter(LOG_LOGFILE_FORMAT))

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(fh)
# add ch to logger
logger.addHandler(ch)
logger.info("++++ loger starts ++++")

if __name__ == '__main__':

    logging.basicConfig(filename='internal.log', level=logging.DEBUG)

    logging.info('Sent using logging from the calling main')
    a = LearnLogging.internal.internal(logger)
    logger.info("LOGGER - Send using logger INFO in main")
    logger.debug("LOGGER - Send using logger DEBUG in main")
