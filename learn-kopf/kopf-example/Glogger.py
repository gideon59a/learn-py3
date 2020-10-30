#!/usr/bin/python
#from __future__ import print_function

# Copied herefrom GGlobal import GGlobal

import datetime
import logging
import os
import re
# import subprocess
import sys
import traceback


# GGlobal
class GGlobal():
    LOG_INDENT_WIDTH   = 3
    LOG_FILE           = 'x.log'
    LOG_FILE_MODE      = 'w+'
    LOG_LOGFILE_FORMAT = '%(asctime)s [%(module)-15.15s] [%(levelname)-6.6s]  %(message)s'
    #LOG_LOGFILE_FORMAT = '[%(module)-15.15s] [%(levelname)-6.6s]  %(message)s'
    LOG_STD_OUT_FORMAT = '%(module)s - %(message)s'

class GLogger():

    def __init__(self,
                 log_file=GGlobal.LOG_FILE,
                 log_file_mode=GGlobal.LOG_FILE_MODE,
                 log_logfile_format=GGlobal.LOG_LOGFILE_FORMAT,
                 log_std_out_format=GGlobal.LOG_STD_OUT_FORMAT,
                 log_level=logging.INFO,
                 secured=True):
        self.log_file = log_file
        self.log_file_mode = log_file_mode
        self.log_file_path = os.path.dirname(self.log_file)
        self.log_logfile_format = log_logfile_format
        self.log_std_out_format = log_std_out_format
        self.log_level = log_level
        self.secured = secured

        self.log = GLogger.get_logger()
        self.log.timer_start = self.log_timer_start
        self.log.timer_end = self.log_timer_end
        self.start_time = None
        self.stop_time = None

        self.log_timer_start()

        # prevent to create multiple handlers
        if not self.log.handlers:
            # this should be always DEBUG
            #xx self.log.setLevel(logging.DEBUG)
            self.log.setLevel(self.log_level)
            self.__set_handlers()

    def log_timer_start(self):
        self.start_time = datetime.datetime.utcnow()

    def log_timer_end(self):
        self.stop_time = datetime.datetime.utcnow()
        if self.start_time and self.log:
            self.log.info('Elapsed time {}'
                          .format(self.stop_time - self.start_time))

    def __set_handlers(self):
        print ("LOG FILE NAME ", self.log_file)
        fh = logging.FileHandler(self.log_file, mode=self.log_file_mode)
        fh.setLevel(self.log_level)
        fh.setFormatter(logging.Formatter(self.log_logfile_format))

        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)
        ch.setFormatter(logging.Formatter(self.log_std_out_format))

        #if self.secured:
            #pf = PasswordFilter()
            #ch.addFilter(pf)
            #fh.addFilter(pf)

        self.log.addHandler(fh)
        self.log.addHandler(ch)  # No need for another screen log

        self.log.debug('GLogger initialized with log_level={} for std_out'
                       .format(logging.getLevelName(self.log_level)))

        # Force to use our exception logging
        sys.excepthook = GLogger.log_exception

    def reset_handlers(self):
        handlers = self.log.handlers[:]
        for handler in handlers:
            handler.close()
            self.log.removeHandler(handler)

        self.__set_handlers()

    @staticmethod
    def indent_message(message):
        return '\t{}'.expandtabs(GGlobal.LOG_INDENT_WIDTH).format(message)

    @staticmethod
    def split(separator, string):
        return filter(bool, re.split(separator, str(string)))

    @staticmethod
    def get_logger(name=__name__):
        return logging.getLogger(name)

    @staticmethod
    def log_exception(exception_type, exception, trace):
        log = GLogger.get_logger()
        trace = ''.join(traceback.format_tb(trace))\
                .replace('    ', '\t').replace('  ', '')

        if exception_type.__name__ == 'KeyboardInterrupt':
            log.exception('{}: execution interrupted by end-user'
                          .format(exception_type.__name__))
            sys.exit(2)
        else:
            if exception_type.__name__ != 'Base':
                exception = '{}: {}'.format(exception_type.__name__, exception)

            log.exception(exception)
            log.exception('Traceback (most recent call last):\n{}'
                          .format(trace))
