#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys
import os
import logging
from conf import config
from interface import rmqclient


def configure_logging(level):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(name)s %(levelname)s %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    root_logger.addHandler(ch)


def signal_handler(signal, frame):
    print('CTRL-C caught')


# configure logging
logger = logging.getLogger(__name__)
configure_logging(logging.INFO)

# set configuration
config.cwd = os.getcwd()

# start ZMQ client
if(config.rabbitmq['active']):
    c = rmqclient.start()

logger.info('Starting mail2run application')

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
signal.pause()

logger.info('Stopping mail2run application')
sys.exit(0)
