from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from sites import models as site_models
from sites.decorators import required_site_access, require_verified_site
from ..forms import NewBenchmarkForm


__all__ = ['NewBenchmarkForSite', 'NewBenchmark']


@method_decorator(required_site_access, name='dispatch')
@method_decorator(require_verified_site, name='dispatch')
class NewBenchmarkForSite(View):
    """View for creating a new benchmark for a given site."""

    def get(
        self,
        request: HttpRequest,
        site: site_models.Site,
        site_access: site_models.SiteAccess
    ) -> HttpResponse:
        """Renders the new benchmark form."""
        form = NewBenchmarkForm(user=request.user, site=site)
        return render(request, 'benchmark/new_benchmark_for_site.html', {
            'form': form,
            'site': site,
        })

    def post(
        self,
        request: HttpRequest,
        site: site_models.Site,
        site_access: site_models.SiteAccess
    ) -> HttpResponse:
        """Handles the POST request."""
        form = NewBenchmarkForm(request.POST, user=request.user, site=site)
        if not form.is_valid():
            messages.error(request, form.errors)
            return HttpResponseRedirect(
                reverse(
                    'benchmark:new_benchmark_for_site',
                    args=[site.id, site.slug]
                )
            )
        form.save()
        return HttpResponseRedirect(
            reverse('sites:site', args=[site.id, site.slug])
        )


@method_decorator(login_required, name='dispatch')
class NewBenchmark(View):
    """View for creating a new benchmark."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Renders the new benchmark form."""
        form = NewBenchmarkForm(user=request.user)
        return render(request, 'benchmark/new_benchmark.html', {
            'form': form,
        })

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handles the POST request."""
        form = NewBenchmarkForm(request.POST, user=request.user)
        if not form.is_valid():
            messages.error(request, form.errors)
            return HttpResponseRedirect(
                reverse('benchmark:new_benchmark_for_site')
            )
        form.save()
        return HttpResponseRedirect(
            reverse('sites:dashboard')
        )
