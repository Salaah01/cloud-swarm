"""Verifies Google recapture."""
import json
import urllib
from django.conf import settings


def verify_recaptcha(recaptchaResponse: str) -> bool:
    """Verifies Google recapture.

    Args:
        recaptchaResponse - (str) The recaptcha response from the POST request.

    Returns:
        bool - Indicates whether the recaptcha has been passed or not.
    """

    # If in test mode then pass the test.
    if settings.CAPTCHA_TEST_MODE or settings.DEBUG:
        return True

    if not recaptchaResponse:
        return False

    verifyURL = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptchaResponse
    }
    data = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request(verifyURL, data=data)

    # verify the token submitted with the form is valid
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    return result.get('success', False)
