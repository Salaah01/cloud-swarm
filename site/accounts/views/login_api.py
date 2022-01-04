"""API for the login function."""

import json
from django.contrib import messages
from django.http import JsonResponse
from core_functions import verify_recaptcha
from accounts import utils


def login_api(request):
    """Login API"""

    # Edge case - reject any non post requests.
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error_type': 'invalid method',
            'error': 'Only compatible with a POST request.'
        })

    post_request = json.loads(request.body)

    # Validate recaptcha
    if not verify_recaptcha(post_request.get('g-recaptcha-response')):
        messages.error(request, 'Recaptcha failed')
        return JsonResponse({
            'success': False,
            'error_type': 'reCAPTCHA',
            'error': 'Failed reCAPTCHA. Please refresh the page and try again.'
        })

    user = utils.login_user(
        request,
        post_request.get('email'),
        post_request.get('password')
    )

    if not user:
        messages.error(request, 'Invalid login details.')
        return JsonResponse({
            'success': False,
            'error_type': 'invalid credentials',
        })

    messages.success(request, 'You are now logged in.')

    return JsonResponse({
        'success': True,
        'user': user.id,
    })
