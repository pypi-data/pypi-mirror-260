""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 10, 2021

@author: pymancer@gmail.com (polyanalitika.ru)
"""
from box import Box

POSTGRESQL_DIALECT = 'postgresql'
MSSQL_DIALECT = 'mssql'
SQLITE_DIALECT = 'sqlite'

QUERY_KEY = 'query'

NoneType = type(None)

QN_DELIMITER = '.'

# fmt: off
WRAP = Box({
    'const': {
        "operation": "+",
        "left": "<+",
        "right": "+>"
    },
    'double': {
        "operation": "=",
        "left": "<=",
        "right": "=>"
    },
    'single': {
        "operation": "-",
        "left": "<-",
        "right": "->"
    },
    'unquote': {
        "operation": "~",
        "left": "<~",
        "right": "~>"
    },
    "lefts": [
        "<+",
        "<=",
        "<-",
        "<~"
    ],
    "rights": [
        "+>",
        "=>",
        "->",
        "~>"
    ],
    "left_escape": "<",
    "right_escape": ">",
    "key_len": 2,
    "quote_len": 1,
    "escape_len": 1,
    "escapes": {
        "left": "<",
        "right": ">"
    },
    "sizes": {
        "key": 2,
        "quote": 1,
        "escape": 1
    }
}, frozen_box=True)

_BASE_DIALECT = {
    "cast": {
        "true": "true",
        "false": "false",
        "null": "null"
    },
    "quote": {
        'double': {
            "left": '"',
            "right": '"',
            "delimiter": QN_DELIMITER
        },
        'single': {
            "left": "'",
            "right": "'",
            "delimiter": None
        }
    }
}

TRANSLATORS = Box({
    POSTGRESQL_DIALECT: _BASE_DIALECT,
    MSSQL_DIALECT: _BASE_DIALECT | {
        "quote": {
            'double': {
                "left": '[',
                "right": ']',
                "delimiter": QN_DELIMITER
            },
            'single': {
                "left": "'",
                "right": "'",
                "delimiter": None
            }
        }
    },
    SQLITE_DIALECT: _BASE_DIALECT | {
        "cast": {
            "true": "1",
            "false": "0",
            "null": "null"
        }
    }
}, frozen_box=True)
# fmt: on
