from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from sites import models as site_models
from sites.decorators import required_site_access
from ..forms import NewBenchmarkForm


@method_decorator(required_site_access, name='dispatch')
class NewBenchmark(View):
    """View for creating a new benchmark."""

    def get(
        self,
        request: HttpRequest,
        site: site_models.Site,
        site_access: site_models.SiteAccess
    ) -> HttpResponse:
        """Renders the new benchmark form."""
        form = NewBenchmarkForm(user=request.user)
        return render(request, 'benchmark/new_benchmark.html', {'form': form})

    def post(
        self,
        request: HttpRequest,
        site: site_models.Site,
        site_access: site_models.SiteAccess
    ) -> HttpResponse:
        """Handles the POST request."""
        form = NewBenchmarkForm(request.POST, user=request.user)
        if not form.is_valid():
            messages.error(request, form.errors)
            return HttpResponseRedirect(
                reverse('benchmark:new_benchmark', args=[site.id, site.slug])
            )
        form.save()
        return HttpResponseRedirect(
            reverse('sites:site', args=[site.id, site.slug])
        )
