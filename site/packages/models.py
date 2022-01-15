from django import dispatch
from django.db import models
from django.core.cache import cache


PACKAGE_PRICE_UPDATED = dispatch.Signal()


class Package(models.Model):
    """Represents a package."""

    ALL_PACKAGES_CACHE_KEY = 'all_packages'
    stripe_product_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text='Do not change this value. Managed by system.'
    )
    stripe_price_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text='Do not change this value. Managed by system.'
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    one_time_package = models.BooleanField(default=False)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_price = self.price

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        cache.delete(self.ALL_PACKAGES_CACHE_KEY)
        price_changed = (
            self._old_price is not None
            and self.price != self._old_price
        )
        super().save(*args, **kwargs)
        if price_changed:
            PACKAGE_PRICE_UPDATED.send(sender=self.__class__, instance=self)

    @ classmethod
    def free_package(cls):
        """Returns the free package."""
        return cls.objects.get(name='Free')

    @ classmethod
    def all(cls):
        """Returns all packages."""
        if cache.get(cls.ALL_PACKAGES_CACHE_KEY):
            return cache.get(cls.ALL_PACKAGES_CACHE_KEY)
        packages = cls.objects.all()
        cache.set(cls.ALL_PACKAGES_CACHE_KEY, packages)
        return packages
