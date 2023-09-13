#!/usr/bin/env python3
"""authentication module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
