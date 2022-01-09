from django.http import HttpRequest, HttpResponse
from . import models as account_models


def account_middleware(get_response):
    """If a user is logged in, add their account to the request."""

    def middleware(request: HttpRequest) -> HttpResponse:
        if request.user and request.user.is_authenticated:
            account = account_models.Account.objects.filter(
                user=request.user
            ).first()
        else:
            account = None
        request.account = account
        return get_response(request)

    return middleware
