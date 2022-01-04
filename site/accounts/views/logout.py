"""Logout view."""

from django.contrib import auth, messages
from django.shortcuts import redirect


def logout(request):
    """Logout view. Log user out and return them to the page that they had
    just come from.
    """
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, 'You have be logged out.')
    else:
        messages.error(request, 'Could not log out, you were not logged in.')

    next_url = request.META.get('HTTP_REFERER')
    if not next_url or 'logout' in next_url:
        next_url = 'index'
    return redirect(next_url)
