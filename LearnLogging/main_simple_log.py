# The purpose is to learn standard logging to use e.g. in docker (using python 3.8.5)
import LearnLogging.internal

import logging
logging.basicConfig(filename='main.log', level=logging.INFO)
logging.debug(' Message sent from the main file')
logging.info('So should this')
logging.warning('And this, too')
logger = logging.getLogger(__name__)
logger.info("LOGGER - Send using logger before start")

LOG_STD_OUT_FORMAT = '%(module)s - %(message)s'

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter(LOG_STD_OUT_FORMAT))

logger = logging.getLogger(__name__)
# add ch to logger
logger.addHandler(ch)

if __name__ == '__main__':

    # The following has no effect, probably because the above basic config while
    # there is no additional getLogger etc.
    logging.basicConfig(filename='internal.log', level=logging.DEBUG)

    logging.info('Sent using logging from the calling main')
    a = LearnLogging.internal.internal(logger)
    logger.info("LOGGER - Send using logger INFO in main")
    logger.debug("LOGGER - Send using logger DEBUG in main")
