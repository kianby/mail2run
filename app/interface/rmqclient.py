#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json
import logging
import re
from threading import Thread
from conf import config

logger = logging.getLogger(__name__)


credentials = pika.PlainCredentials(
    config.rabbitmq['username'], config.rabbitmq['password'])
connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq['host'], port=config.rabbitmq[
                                     'port'], credentials=credentials, virtual_host=config.rabbitmq['vhost']))


def mail(to_email, subject, message):

    body = {
        'to': to_email,
        'subject': subject,
        'content': message
    }
    channel = connection.channel()
    channel.basic_publish(exchange=config.rabbitmq['exchange'],
                          routing_key='mail.command.send',
                          body=json.dumps(body, indent=False, sort_keys=False))
    connection.close()
    logger.info('Email for %s posted' % to_email)


def send_delete_command(content):

    channel = connection.channel()
    channel.basic_publish(exchange=config.rabbitmq['exchange'],
                          routing_key='mail.command.delete',
                          body=json.dumps(content, indent=False, sort_keys=False))
    connection.close()
    logger.info('Email accepted. Delete request sent for %s' % content)


def process_message(chan, method, properties, body):
    topic = method.routing_key
    data = json.loads(body)

    if topic == 'mail.message':
        logger.info('new message => {}'.format(data))

        for run in config.runs:
            if re.search(run['regex'], data['subject']):

                try:
                    r = subprocess.run(
                        ["ls", "-l", "/dev/null"], stdout=subprocess.PIPE)
                    message = str(r)
                except:
                    logger.exception('cannot execute')
                    message = 'cannot execute {}'.format(run['exec'])

                send_delete_command(data)

                mail(data['from'], 'RE: ' + data['subject'], message)
                break
            else:
                logger.info('no match {} for {}'.format(data['subject'], run))
    else:
        logger.warn('unsupported message [topic={}]'.format(topic))


class CommandConsumer(Thread):

    def run(self):

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
