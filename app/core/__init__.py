#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
from interface import rmqclient
from conf import config

# configure logging
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


# configure logging
logger = logging.getLogger(__name__)
configure_logging(logging.INFO)

# set configuration
config.cwd = os.getcwd()

# start ZMQ client
if(config.rabbitmq['active']):
    c = rmqclient.start()


logger.info('Starting mail2run application')

input("\nPress Enter to stop.")

logger.info('Stopping mail2run application')
sys.exit(0)
