#!/usr/bin/env python3
"""
Filtered Logger Module
"""
import re


def filter_datum(fields: list[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message
