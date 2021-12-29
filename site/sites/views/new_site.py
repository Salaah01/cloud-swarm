from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.urls import reverse
from .. import forms


class NewSite(View):
    """View for registering a new site."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """GET request handler."""
        form = forms.NewSiteForm()
        return render(request, 'sites/new_site.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """POST request handler."""
        form = forms.NewSiteForm(request.POST, user=request.user)
        if not form.is_valid():
            messages.error(request, form.errors)
            return render(request, 'sites/new_site.html', {'form': form})
        site = form.save(request.user)
        messages.success(request, 'Site created.')
        return HttpResponseRedirect(
            reverse('sites:site', args=[site.id, site.slug])
        )
