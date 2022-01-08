import typing as _t
from django import forms
from sites import models as site_models
from . import models as benchmark_models


class NewBenchmarkForm(forms.ModelForm):
    """Form for creating a new benchmark."""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        site = (kwargs.pop('site', None))
        super().__init__(*args, **kwargs)
        self.setup_site_field(site)

        # Add a class to all fields.
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def setup_site_field(self, site: _t.Optional[site_models.Site]):
        if site:
            self.fields['site'].initial = site
            self.fields['site'].widget = forms.HiddenInput()
            self.fields['site'].required = False
        else:
            self.fields['site'].queryset = site_models.Site.for_user(
                self.user,
                site_models.SiteAccess.AuthLevels.MANAGER
            )
        self.fields['site'].empty_label = None

    def clean_site(self):
        site = self.cleaned_data['site']
        if site is None:
            raise forms.ValidationError(
                'Please select a site.',
                code='invalid'
            )

        user_access = site_models.SiteAccess.user_access(site, self.user)
        if user_access is None:
            raise forms.ValidationError(
                'You do not have access to this site.',
                code='invalid'
            )
        if not user_access.user_has_manager_access():
            raise forms.ValidationError(
                'You do not have access to benchmark this site.',
                code='invalid'
            )

        if not site.verify():
            raise forms.ValidationError(
                'Site not verified.',
                code='invalid'
            )
        return site

    def save(self, *args, **kwargs):
        benchmark = super().save(commit=False)
        benchmark.requested_by = self.user
        benchmark.save()
        return benchmark

    class Meta:
        model = benchmark_models.Benchmark
        fields = ['site', 'num_servers', 'num_requests']
