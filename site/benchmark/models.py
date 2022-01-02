import typing as _t
from datetime import timedelta
from django import dispatch
from django.db import models
from django.contrib.auth.models import User
from sites import models as site_models


NEW_BENCHMARK = dispatch.Signal()
UPDATED_BENCHMARK_PROGRESS = dispatch.Signal()


class Benchmark(models.Model):
    """Represents a benchmark."""
    site = models.ForeignKey(
        site_models.Site,
        on_delete=models.CASCADE,
        related_name='benchmarks'
    )
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

    @classmethod
    def avg_completion_time(cls) -> _t.Union[timedelta, None]:
        """Return the average completion time for all benchmarks."""
        records = cls.objects.filter(
            started_on__isnull=False,
            completed_on__isnull=False
        )
        if records.count() == 0:
            return None
        total_seconds = sum(
            (record.completed_on - record.started_on).total_seconds()
            for record in records
        )
        records_count = records.count()
        return timedelta(seconds=total_seconds / records_count)


class BenchmarkProgress(models.Model):
    """Represents the progress of a benchmark."""

    class StatusChoices(models.IntegerChoices):
        """Represents the status of a benchmark."""
        PENDING = 0, 'Pending'
        PROVISIONING = 1, 'Provisioning servers'
        SERVER_SETUP = 2, 'Setting up servers'
        SCHEDULING = 3, 'Scheduling benchmark'
        RUNNING = 4, 'Running benchmark'
        RESULTS = 5, 'Collecting results'
        COMPLETED = 6, 'Completed'

    LOGGABLE_STATUSES = (
        (StatusChoices.SCHEDULING, 'scheduled_on'),
        (StatusChoices.COMPLETED, 'completed_on'),
    )

    benchmark = models.OneToOneField(
        Benchmark,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    status = models.PositiveIntegerField(
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    class Meta:
        verbose_name_plural = 'Benchmark Progress'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._status = self.status

    def __str__(self):
        return f'{self.get_status_display()} for {self.benchmark}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._status != self.status:
            self._status = self.status
            UPDATED_BENCHMARK_PROGRESS.send(
                sender=self.__class__,
                instance=self
            )

    def set_completed(self) -> None:
        """Set the benchmark progress to completed."""
        self.status = self.StatusChoices.COMPLETED
        self.save()
