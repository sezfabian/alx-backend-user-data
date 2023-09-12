#!/usr/bin/env python3
"""Authentication module."""
from flask import request
from typing import List


class Auth:
    """Class for authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if user is authenticated."""
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[len(path) - 1] != "/":
            path = path + "/"

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header."""
        return None

    def current_user(self, request=None) -> str:
        """Current user."""
        return None
