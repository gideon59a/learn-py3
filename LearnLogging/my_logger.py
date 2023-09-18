#!/usr/bin/python
from __future__ import print_function

# Copied herefrom GGlobal import GGlobal

import datetime
import logging
import os
import re
# import subprocess
import sys
import traceback


# GGlobal
LOG_INDENT_WIDTH   = 3
LOG_FILE           = 'x.log'
LOG_FILE_MODE      = 'w+'
LOG_LOGFILE_FORMAT = '%(asctime)s [%(module)-15.15s] [%(levelname)-6.6s]  %(message)s'
#LOG_LOGFILE_FORMAT = '[%(module)-15.15s] [%(levelname)-6.6s]  %(message)s'
LOG_STD_OUT_FORMAT = '%(module)s - %(message)s'

class GLogger():

    def __init__(self,
                 log_file=LOG_FILE,
                 log_file_mode=LOG_FILE_MODE,
                 log_logfile_format=LOG_LOGFILE_FORMAT,
                 log_std_out_format=LOG_STD_OUT_FORMAT,
                 log_level=logging.INFO,
                 file_log_level=logging.DEBUG):
        self.log_file = log_file
        self.log_file_mode = log_file_mode
        self.log_file_path = os.path.dirname(self.log_file)
        self.log_logfile_format = log_logfile_format
        self.log_std_out_format = log_std_out_format
        self.log_level = log_level
        self.file_log_level = file_log_level

        self.log = GLogger.get_logger()  # = logging.getLogger(__name__)
        self.log.timer_start = self.log_timer_start
        self.log.timer_end = self.log_timer_end
        self.start_time = None
        self.stop_time = None

        self.log_timer_start()

        # prevent to create multiple handlers
        if not self.log.handlers:
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
        print("LOG FILE NAME ", self.log_file, "file_log_level:", self.file_log_level)
        self.fh = logging.FileHandler(self.log_file, mode=self.log_file_mode)
        self.fh.setLevel(self.file_log_level)
        self.fh.setFormatter(logging.Formatter(self.log_logfile_format))

        self.ch = logging.StreamHandler()
        self.ch.setLevel(self.log_level)
        self.ch.setFormatter(logging.Formatter(self.log_std_out_format))

        self.log.addHandler(self.fh)  # to log file
        self.log.addHandler(self.ch)  # to screen log

        #print("LOG HERE *******")
        ###fh.setLevel(logging.DEBUG)  #### HAS NO EFFECT
        self.log.debug('GLogger initialized with log_level={} for std_out'
                       .format(logging.getLevelName(self.log_level)))

    #def set_log_level(self, log_level):
    #    self.fh.setLevel(log_level)
    #    self.ch.setLevel(log_level)

    @staticmethod
    def get_logger(name=__name__):
        return logging.getLogger(name)
