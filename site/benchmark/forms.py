import typing as _t
from django import forms
from sites import models as site_models
from . import models as benchmark_models


class NewBenchmarkForm(forms.ModelForm):
    """Form for creating a new benchmark."""

    class Meta:
        model = benchmark_models.Benchmark
        fields = ['site', 'num_servers', 'num_requests']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        self.site = (kwargs.pop('site', None))
        super().__init__(*args, **kwargs)
        self.setup_site_field(self.site)

        # Add a class to all fields.
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def setup_site_field(self, site: _t.Optional[site_models.Site]):
        if site:
            self.fields['site'].initial = site
            self.fields['site'].widget = forms.HiddenInput()
            self.fields['site'].required = False
            self.fields['site'].value = site
        else:
            self.fields['site'].queryset = site_models.Site.for_account(
                self.account,
                site_models.SiteAccess.AuthLevels.MANAGER
            )
        self.fields['site'].empty_label = None

    def clean_site(self):
        site = self.cleaned_data['site'] or self.site
        if site is None:
            raise forms.ValidationError(
                'Please select a site.',
                code='invalid'
            )

        account_access = site_models.SiteAccess.account_access(
            site,
            self.account
        )
        if account_access is None:
            raise forms.ValidationError(
                'You do not have access to this site.',
                code='invalid'
            )
        if not account_access.account_has_manager_access():
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

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        self.clean_account()
        return cleaned_data

    def clean_account(self):
        if not self.account.can_run_benchmark:
            raise forms.ValidationError(
                'You cannot run anymore benchmarks as you have exceeded your '
                'quota'
            )

    def save(self, *args, **kwargs):
        benchmark = super().save(commit=False)
        benchmark.requested_by = self.account
        benchmark.save()
        return benchmark
