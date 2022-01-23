"""Register page."""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.conf import settings
from core_functions import verify_recaptcha
# from accounts.models import CommPrefs
from accounts import utils


def register(request):
    """Register page."""

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':

        # Validate recaptcha
        if not verify_recaptcha(request.POST.get('g-recaptcha-response')):
            messages.error(request, 'Recaptcha failed')
            return redirect('register')

        # Check that the terms and conditions have been accepted.
        if not request.POST.get('termsAccepted'):
            messages.error(request, 'You must accept the terms and conditions')
            return redirect('register')

        user_sign_up = utils.sign_up_user(
            request,
            request.POST.get('email'),
            request.POST.get('first-name'),
            request.POST.get('last-name'),
            request.POST.get('password'),
            request.POST.get('password-confirm')
        )

        if not user_sign_up.success:
            messages.error(request, user_sign_up.error)
            return redirect('register')

        messages.success(
            request, 'Congratulations! You have been registered')
        return redirect('index')

    else:
        context = {
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
            'recaptcha_action': 'sign_up'
        }
        return render(request, 'accounts/register.html', context)
