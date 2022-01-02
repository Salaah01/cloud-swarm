"""Handles JWT operations."""

import os
import jwt


def create_jwt(payload: dict) -> str:
    """Creates a JWT token.
    Args:
        payload: The payload to encode.
    Returns:
        The encoded token.
    """
    return jwt.encode(
        payload,
        os.environ['JWT_SECRET_KEY'],
        algorithm='HS256'
    )
