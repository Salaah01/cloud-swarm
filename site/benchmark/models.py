from django import dispatch
from django.db import models
from django.contrib.auth.models import User
from sites import models as site_models


NEW_BENCHMARK = dispatch.Signal()


class Benchmark(models.Model):
    """Represents a benchmark."""
    site = models.ForeignKey(site_models.Site, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    num_servers = models.PositiveIntegerField(
        default=1,
        verbose_name='Number of Servers'
    )
    num_requests = models.PositiveIntegerField(
        default=1,
        verbose_name='Number of Requests',
        help_text='Number of requests per server'
    )
    started_on = models.DateTimeField(null=True, blank=True)
    scheduled_on = models.DateTimeField(null=True, blank=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    min_time = models.PositiveIntegerField(blank=True, null=True)
    max_time = models.PositiveIntegerField(blank=True, null=True)
    mean_time = models.PositiveIntegerField(blank=True, null=True)
    completed_requests = models.PositiveIntegerField(blank=True, null=True)
    failed_requests = models.PositiveIntegerField(blank=True, null=True)
    sys_error_requests = models.PositiveIntegerField(
        help_text='The number of requests that failed due to a system error.',
        blank=True,
        null=True,
        verbose_name='System Error Requests'
    )

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Benchmark'

    def __str__(self):
        return f'[{self.created_on.strftime("%Y-%m-%d %H:%M")}] {self.site}'

    def save(self, *args, **kwargs):
        """Save the benchmark and publish a new benchmark event if this is a
        new benchmark.
        """
        created = self.pk is None
        super().save(*args, **kwargs)
        if created:
            NEW_BENCHMARK.send(sender=self.__class__, instance=self)

    @classmethod
    def for_site(cls, site: site_models.Site):
        """Return all benchmark queues for a site."""
        return cls.objects.filter(site=site)

    @classmethod
    def for_user(cls, user: User):
        """Return all benchmark queues for a user."""
        return cls.objects.filter(requested_by=user)

    @classmethod
    def not_started(cls):
        """Return all sites that have not been started."""
        return cls.objects.filter(started_on__isnull=True)

    @classmethod
    def started(cls):
        """Return all sites that have been started."""
        return cls.objects.filter(started_on__isnull=False)

    @classmethod
    def scheduled(cls):
        """Return all sites that have been scheduled."""
        return cls.objects.filter(scheduled_on__isnull=False)

    @classmethod
    def not_scheduled(cls):
        """Return all sites that have not been scheduled."""
        return cls.objects.filter(scheduled_on__isnull=True)

    @classmethod
    def completed(cls):
        """Return all sites that have been completed."""
        return cls.objects.filter(completed_on__isnull=False)

    @classmethod
    def not_completed(cls):
        """Return all sites that have not been completed."""
        return cls.objects.filter(completed_on__isnull=True)
