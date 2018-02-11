#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json
import logging
import re
from threading import Thread
from conf import config

logger = logging.getLogger(__name__)


def process_message(chan, method, properties, body):
    topic = method.routing_key
    data = json.loads(body)

    if topic == 'mail.message': 
        logger.info('new message => {}'.format(data))

        for run in config.runs:
            if re.search(run['regex'], data['subject']):
                logger.info('execute {}'.format(run))
                break
    else:
        logger.warn('unsupported message [topic={}]'.format(topic))


class CommandConsumer(Thread):

    def run(self):

        credentials = pika.PlainCredentials(
            config.rabbitmq['username'], config.rabbitmq['password'])
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq['host'], port=config.rabbitmq[
                                             'port'], credentials=credentials, virtual_host=config.rabbitmq['vhost']))

        channel = connection.channel()
        channel.exchange_declare(exchange=config.rabbitmq['exchange'],
                                 exchange_type='topic')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=config.rabbitmq['exchange'],
                           queue=queue_name,
                           routing_key='mail.message')
        channel.basic_consume(process_message,
                              queue=queue_name,
                              no_ack=True)
        channel.start_consuming()


def start():
    consumer = CommandConsumer()
    consumer.start()