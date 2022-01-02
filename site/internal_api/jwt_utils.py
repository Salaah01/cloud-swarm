"""Handles JWT operations."""

from django.conf import settings
import jwt


def decode_jwt(token: str) -> dict:
    """Decodes a JWT token.
    Args:
        token: The JWT token to decode.
    Returns:
        The decoded token.
    """
    try:
        return {
            'success': True,
            'payload': jwt.decode(
                token,
                settings.JWT['JWT_SECRET_KEY'],
                algorithms=[settings.JWT['JWT_ALGORITHM']]
            )
        }
    except jwt.ExpiredSignatureError:
        return {
            'success': False,
            'error': 'Token expired.'
        }
    except jwt.InvalidTokenError:
        return {
            'success': False,
            'error': 'Invalid token.'
        }
