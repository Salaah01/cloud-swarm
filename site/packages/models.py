from django.db import models


class Package(models.Model):
    """Represents a package."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    package_duration = models.IntegerField(
        help_text='Period (Days) until package expires',
        null=True,
        blank=True
    )
    instances = models.PositiveIntegerField(
        help_text='Number of instances per benchmark.',
    )
    requests = models.PositiveIntegerField(
        help_text='Number of requests per instance.',
    )
    refresh_period = models.PositiveIntegerField(
        help_text='Number of days between benchmark limits refresh.',
    )
    quota = models.PositiveIntegerField(
        help_text='Number of benchmarks allowed before the refresh period.',
    )

    def __str__(self):
        return self.name
