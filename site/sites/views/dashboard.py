from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from sites import models as site_models


def dashboard(request: HttpRequest) -> HttpResponse:
    """Dashboard where user is able to see their registered sites and register
    new sites.
    """
    sites = site_models.Site.for_user(request.user)
    return render(request, 'sites/dashboard.html', {'sites': sites})
