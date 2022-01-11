from django.db import models
from django.core.cache import cache


class Package(models.Model):
    """Represents a package."""

    ALL_PACKAGES_CACHE_KEY = 'all_packages'

    name = models.CharField(max_length=100, unique=True)
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

    def save(self, *args, **kwargs):
        cache.delete(self.ALL_PACKAGES_CACHE_KEY)
        super().save(*args, **kwargs)

    @classmethod
    def free_package(cls):
        """Returns the free package."""
        return cls.objects.get(name='Free')

    @classmethod
    def all(cls):
        """Returns all packages."""
        if cache.get(cls.ALL_PACKAGES_CACHE_KEY):
            return cache.get(cls.ALL_PACKAGES_CACHE_KEY)
        packages = cls.objects.all()
        cache.set(cls.ALL_PACKAGES_CACHE_KEY, packages)
        return packages
