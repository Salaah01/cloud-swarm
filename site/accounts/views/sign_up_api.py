"""API for the sign up function."""

import json
from django.contrib import messages
from django.http import JsonResponse
from core_functions import verify_recaptcha, dataclasses
from accounts import utils
# from accounts.models import CommPrefs


def sign_up_api(request):
    """Sign up API."""

    # Edge case - reject any non post requests.
    if request.method != 'POST':
        return dataclasses.APIResponse(
            success=False,
            error_type='Invalid method',
            error='Only compatible with a POST request.'
        ).as_json_response(405)

    post_request = json.loads(request.body)

    # Validate recaptcha
    if not verify_recaptcha(post_request.get('g-recaptcha-response')):
        messages.error(request, 'Recaptcha failed')
        return dataclasses.APIResponse(
            success=False,
            error_type='reCAPTCHA',
            error='Failed reCAPTCHA. Please refresh the page and try again.'
        ).as_json_response()

    # Check that the terms and conditions have been accepted.
    # if not post_request.get(commPrefKeys['termsAccepted']):
    #     messages.error(request, 'Terms and conditions not accepted')
    #     return dataclasses.APIResponse(
    #         success=False,
    #         error_type='Terms and conditions not accepted',
    #         error='Terms and conditions have not been accepted.'
    #     ).as_json_response()

    user_sign_up = utils.sign_up_user(
        request,
        post_request.get('email'),
        post_request.get('firstName'),
        post_request.get('lastName'),
        post_request.get('password'),
        post_request.get('confirmPassword')
    )

    if not user_sign_up.success:
        return user_sign_up.as_json_response()

    user = user_sign_up.retuned_object

    # Update the user's communication preferences.
    # CommPrefs.objects.create(
    #     user=user,
    #     promotions=post_request.get(commPrefKeys['promotions'], False),
    #     blogs=post_request.get(commPrefKeys['blogs'], False),
    #     newsletters=post_request.get(commPrefKeys['newsletters'], False),
    # ).save()

    return JsonResponse({'success': True, 'user': user.id})
