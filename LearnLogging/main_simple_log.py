# The purpose is to learn standard logging to use e.g. in docker (using python 3.8.5)
import LearnLogging.internal

import logging
logging.basicConfig(filename='main.log', level=logging.DEBUG)
logging.debug(' Message sent from the main file')
# logging.info('So should this')
# logging.warning('And this, too')
logger = logging.getLogger(__name__)




if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='internal.log', level=logging.DEBUG)
    logging.debug('Sent from the calling main')
    a = LearnLogging.internal.internal(logger)