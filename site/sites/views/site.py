from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .. import models as site_models
from ..decorators import required_site_access


@required_site_access
def site(
    request: HttpRequest,
    site: site_models.Site,
    site_access: site_models.SiteAccess
) -> HttpResponse:

    if site.previously_verified and not site.verified:
        site.verify()
    return render(request, 'sites/site.html', {
        'site': site,
        'site_access': site_access
    })
