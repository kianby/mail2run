#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json
import logging
import re
import subprocess
from threading import Thread
from conf import config
from util import rabbit

logger = logging.getLogger(__name__)


def get_rabbitmq_connection():

    credentials = pika.PlainCredentials(
        config.rabbitmq['username'], config.rabbitmq['password'])
    parameters = pika.ConnectionParameters(
        host=config.rabbitmq['host'],
        port=config.rabbitmq['port'],
        credentials=credentials,
        virtual_host=config.rabbitmq['vhost']
    )
    return rabbit.Connection(parameters)


def mail(to_email, subject, message):

    body = {
        'to': to_email,
        'subject': subject,
        'content': message
    }
    connector = get_rabbitmq_connection()
    connection = connector.open()
    channel = connection.channel()
    channel.basic_publish(exchange=config.rabbitmq['exchange'],
                          routing_key='mail.command.send',
                          body=json.dumps(body, indent=False, sort_keys=False))
    connector.close()
    logger.info('Email for %s posted' % to_email)


def send_delete_command(content):

    connector = get_rabbitmq_connection()
    connection = connector.open()
    channel = connection.channel()
    channel.basic_publish(exchange=config.rabbitmq['exchange'],
                          routing_key='mail.command.delete',
                          body=json.dumps(content, indent=False, sort_keys=False))
    connector.close()
    logger.info('Email accepted. Delete request sent for %s' % content)


class MailConsumer(rabbit.Consumer):

    def process(self, channel, method, properties, body):
        topic = method.routing_key
        data = json.loads(body)

        if topic == 'mail.message':
            logger.info('new message => {}'.format(data))

            for run in config.runs:
                if re.search(run['regex'], data['subject']):

                    try:
                        r = subprocess.run(
                            [run['exec']], stdout=subprocess.PIPE)
                        message = str(r)
                    except:
                        logger.exception('cannot execute')
                        message = 'cannot execute {}'.format(run['exec'])

                    send_delete_command(data)

                    mail(data['from'], 'RE: ' + data['subject'], message)
                    break
                else:
                    logger.info('no match {} for {}'.format(
                        data['subject'], run))
        else:
            logger.warn('unsupported message [topic={}]'.format(topic))


def start():
    connection = get_rabbitmq_connection()
    c = MailConsumer(connection, config.rabbitmq['exchange'], 'mail.message')
    c.start()
