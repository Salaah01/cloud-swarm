"""Login page."""
from django.contrib import messages
from django.shortcuts import redirect, render
from django.conf import settings
from core_functions import verify_recaptcha
from accounts import utils


def login(request):
    """Login page."""

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':

        # Validate recaptcha
        if not verify_recaptcha(request.POST.get('g-recaptcha-response')):
            messages.error(request, 'Recaptcha failed')
            return redirect('login')

        user = utils.login_user(
            request,
            request.POST.get('email'),
            request.POST.get('password')
        )

        if user:
            messages.success(request, "You are now logged in")
            return redirect(request.POST.get('next', 'index'))
        else:
            messages.error(
                request,
                'Email and/or password did not match our records'
            )
            return redirect('login')

    else:
        context = {
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
            'recaptcha_action': 'login',
            'next': request.GET.get('next')
        }
        return render(request, 'accounts/login.html', context)
