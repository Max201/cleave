#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime


class Log(object):
    DEBUG = True

    # Console colors output
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def message(msg):
        print datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ') + str(msg)

    @staticmethod
    def debug(msg):
        if Log.DEBUG is True:
            Log.message('[DEBUG]    ' + str(msg))

    @staticmethod
    def info(msg):
        Log.message('[INFO]     ' + Log.OKBLUE + str(msg) + Log.ENDC)

    @staticmethod
    def warning(msg):
        Log.message('[WARNING]  ' + Log.WARNING + str(msg) + Log.ENDC)

    @staticmethod
    def error(msg):
        Log.message('[ERROR]    ' + Log.FAIL + str(msg) + Log.ENDC)

    @staticmethod
    def critical(msg):
        Log.message('[CRITICAL] ' + Log.FAIL + Log.BOLD + str(msg) + Log.ENDC)

    @staticmethod
    def disable():
        Log.DEBUG = False

    @staticmethod
    def enable():
        Log.DEBUG = True


__all__ = ['Log']
