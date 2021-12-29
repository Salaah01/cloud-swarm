from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .. import models as site_models


@login_required
def site(request: HttpRequest, id: int, slug: str) -> HttpResponse:
    """Site view."""
    site = site_models.Site.for_id_slug(id, slug)
    if site is None:
        raise Http404()
    user_access = site_models.SiteAccess.user_access(site, request.user)
    if user_access is None:
        raise Http404()

    return render(request, 'sites/site.html', {
        'site': site,
        'user_access': user_access}
    )
