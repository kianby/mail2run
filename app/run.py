#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
from clize import clize, run
from conf import config, schema
from jsonschema import validate


def load_json(filename):
    jsondoc = None
    with open(filename, 'rt') as json_file:
        jsondoc = json.loads(json_file.read())
    return jsondoc


@clize
def mail2run(config_pathname):

    # load and validate startup config
    conf = load_json(config_pathname)
    json_schema = json.loads(schema.json_schema) 
    validate(conf, json_schema)
    
    # set configuration
    config.runs = conf['runs']
    config.rabbitmq = conf['rabbitmq']

    # start application
    from core import app

if __name__ == '__main__':
    run(mail2run)
