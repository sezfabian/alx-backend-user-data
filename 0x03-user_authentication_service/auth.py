#!/usr/bin/env python3
"""authentication module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register new user
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))

        except NoResultFound:
            hashed_password = _hash_password(password)

            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Try locating the user by email.
        If it exists, check the password with bcrypt.checkpw.
        If it matches return True.
        In any other case, return False.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
        except (NoResultFound, InvalidRequestError):
            return False

        return False
