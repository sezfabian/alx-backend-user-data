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
