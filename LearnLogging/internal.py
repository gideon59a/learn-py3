import logging

def internal(logger):
    logger.debug("*** DEBUG INTERNAL Using logger in the internal module")
    logger.info("*** INFO INTERNAL Using logger in the internal module")
    # The below would not be logged
    # logging.info("Using logging (rather than logger) in the internal module")
    return 7


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='internal.log', level=logging.DEBUG)
    logging.debug('Sent from the calling main')
    ilogger = logging.getLogger(__name__)
    a = internal(ilogger)



