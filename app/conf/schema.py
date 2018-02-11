#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with https://app.quicktype.io
#   name: mail2run

json_schema = """
{
    "$ref": "#/definitions/Mail2Run",
    "definitions": {
        "Rabbitmq": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "active": {
                    "type": "boolean"
                },
                "host": {
                    "type": "string"
                },
                "port": {
                    "type": "integer"
                },
                "username": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
                "vhost": {
                    "type": "string"
                },
                "exchange": {
                    "type": "string"
                }
            },
            "required": [
                "active",
                "exchange",
                "host",
                "password",
                "port",
                "username",
                "vhost"
            ],
            "title": "rabbitmq"
        },
        "Run": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "regex": {
                    "type": "string"
                },
                "exec": {
                    "type": "string"
                }
            },
            "required": [
                "exec",
                "regex"
            ],
            "title": "run"
        },
        "Mail2Run": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "rabbitmq": {
                    "$ref": "#/definitions/Rabbitmq"
                },
                "runs": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Run"
                    }
                }
            },
            "required": [
                "rabbitmq",
                "runs"
            ],
            "title": "mail2run"
        }
    }
}
"""