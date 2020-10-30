
def internal(logger):
    logger.info(" Message 2")
    return 7


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='internal.log', level=logging.DEBUG)
    logging.debug('Sent from the calling main')
    logger = logging.getLogger(__name__)
    a = internal(logger)


