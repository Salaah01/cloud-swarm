from django import forms
from sites import models as site_models
from . import models as benchmark_models


class NewBenchmarkForm(forms.ModelForm):
    """Form for creating a new benchmark."""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # Limit sites to those that the user has access to.
        self.fields['site'].queryset = site_models.Site.for_user(
            self.user,
            site_models.SiteAccess.AuthLevels.MANAGER
        )
        self.fields['site'].empty_label = None

        # Add a class to all fields.
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs):
        benchmark = super().save(commit=False)
        benchmark.requested_by = self.user
        benchmark.save()
        return benchmark

    class Meta:
        model = benchmark_models.Benchmark
        fields = ['site', 'num_servers', 'num_requests']
