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

    def save(self, *args, **kwargs):
        benchmark = super().save(commit=False)
        benchmark.requested_by = self.user
        benchmark.save()
        return benchmark

    class Meta:
        model = benchmark_models.Benchmark
        fields = ['site', 'num_servers', 'num_requests']
