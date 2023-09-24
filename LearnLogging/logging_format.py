import logging

LOG_LOGFILE_FORMAT = '%(asctime)s my-container [%(module)-15.15s] [%(levelname)-6.6s]  %(message)s'
logging.basicConfig(filename='format.log', level=logging.DEBUG, format=LOG_LOGFILE_FORMAT)
logging.info('Sent using logging from the calling main')