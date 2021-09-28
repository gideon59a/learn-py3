import logging.handlers

class Alogger():
    def __init__(self, log_file: str, file_level=logging.debug, console_level=logging.debug):
        self.log_file = log_file

    def get_logger(self):
        # create logger
        logger = logging.getLogger(__name__)
        #logger = logging.getLogger('main log')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(self.log_file, 'w+')
        fh.setLevel(logging.DEBUG)
        # create console handler with a different log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        logger.info("trying printing info 1")
        logger.error("trying printing error")
        return logger
