import json
from functools import wraps
from django import http
from django.views.decorators.csrf import csrf_exempt
from .jwt_utils import decode_jwt


def validate_jwt_payload(func):
    """Decorator to validate the JWT payload."""
    @wraps(func)
    def wrapper(
        request: http.HttpRequest,
        *args,
        **kwargs
    ) -> http.HttpResponse:
        """Wrapper function.
        Args:
            request (HttpRequest): The request object.
        """

        # Decode the JWT token.
        payload = decode_jwt(json.loads(request.body)['token'])

        if not payload['success']:
            return http.JsonResponse(payload, status=400)
        return func(request, payload['payload'], *args, **kwargs)
    return csrf_exempt(wrapper)
