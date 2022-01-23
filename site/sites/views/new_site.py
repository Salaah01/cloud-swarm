from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .. import forms


@method_decorator(login_required, name='dispatch')
class NewSite(View):
    """View for registering a new site."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """GET request handler."""
        form = forms.NewSiteForm()
        return render(request, 'sites/new_site.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """POST request handler."""
        form = forms.NewSiteForm(request.POST, account=request.account)
        if not form.is_valid():
            messages.error(request, form.errors)
            return render(request, 'sites/new_site.html', {'form': form})
        site = form.save()
        messages.success(request, 'Site created.')
        return HttpResponseRedirect(
            reverse('site', args=[site.id, site.slug])
        )
