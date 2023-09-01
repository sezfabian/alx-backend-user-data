#!/usr/bin/env python3i
"""
Filtered Logger Module
"""
from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        for field in fields:
            message = re.sub(field + '=.*?' + separator,
                             field + '=' + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """"Filter values in incoming log records using filter_datum
            """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Creates logger object for user dasta
        """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    logger.propagate = False
    return logger
