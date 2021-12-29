import re
from django import forms
from . import models as site_models


class NewSiteForm(forms.ModelForm):
    """Form for registering a new site."""

    class Meta:
        model = site_models.Site
        exclude = (
            'slug',
            'created_on',
            'last_benchmarked',
            'txt_record'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if not cleaned_data.get('domain'):
            return cleaned_data
        if site_models.SiteAccess.objects.filter(
            user=self.user,
            site__domain=cleaned_data['domain']
        ).exists():
            raise forms.ValidationError(
                'You already have access to this site.'
            )
        return cleaned_data

    def clean_domain(self):
        # Check that the domain is valid.
        domain = self.cleaned_data['domain']
        if not re.match(r'^[a-z0-9-]+\.[a-z]{2,}$', domain):
            raise forms.ValidationError(
                'The domain must be a valid domain name.'
            )

        # Remove the "http(s)://" and "www." from the domain.
        domain = re.sub(r'^https?://www.', '', domain).rstrip('/')

        # Covert to lowercase.
        domain = domain.lower()
        return domain

    def save(self, *args, **kwargs):
        # When a new site is created, set the user as a owner.
        site = super().save(*args, **kwargs)

        # A user should exist, but just in case.
        if self.user:
            site.add_user(self.user, site_models.SiteAccess.AuthLevels.ADMIN)

        return site
