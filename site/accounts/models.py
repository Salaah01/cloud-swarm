from datetime import datetime, timedelta
from django import dispatch
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from packages import models as package_models


NEW_ACCOUNT_PACKAGE = dispatch.Signal()


class ActiveManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(
            paid_on__isnull=False,
            created_on__lt=timezone.now(),
            expiry_date__isnull=False,
            expiry_date__gt=timezone.now()
        )


class Account(models.Model):
    """Represents a package associated with an account."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    package = models.ForeignKey(
        package_models.Package,
        on_delete=models.PROTECT,
    )
    expiry_date = models.DateField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._package = self.package
        self._expiry_date = self.expiry_date

    def __str__(self):
        return f'{self.user} - {self.package}'

    def save(self, *args, **kwargs):
        """Overrides the save method. If the package or expiry date has
        changed, then send a signal to add a new history record.
        """
        changed = any([
            not self.id,
            self._package != self.package,
            self._expiry_date != self.expiry_date,
        ])
        instance = super().save(*args, **kwargs)
        if changed:
            NEW_ACCOUNT_PACKAGE.send(sender=self.__class__, instance=self)
        return instance

    @property
    def latest_history(self) -> datetime:
        """Returns the latest package history record."""
        return self.package_history.latest('created_on')

    @property
    def remaining_quota(self):
        """Number of benchmarks that can be run before the next refresh."""
        package_history = self.package_history.active()

        # Scenario where user does not have any paid packages. Thus, check
        # remaining quota on their free package.
        if not package_history:
            return self.package.quota - self.benchmarks.filter(
                created_on__gte=self.latest_history.created_on
            ).count()

        # Scenario where user has paid packages.
        start_date = package_history.earliest('created_on').created_on
        total_quota = package_history.aggregate(
            models.Sum('package__quota')
        )['package__quota__sum']
        return total_quota - self.benchmarks.filter(
            created_on__gte=start_date
        ).count()

    @property
    def can_run_benchmark(self) -> bool:
        """Determine if the account can run another benchmark."""
        return self.remaining_quota > 0

    @classmethod
    def new_free_account(cls, user: User):
        """Create a new free account for the given user."""
        return cls.objects.create(
            user=user,
            package=package_models.Package.objects.get(name='Free'),
        )


class PackageHistory(models.Model):
    """Represents the package history of an account."""
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='package_history'
    )
    package = models.ForeignKey(
        package_models.Package,
        on_delete=models.PROTECT,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    paid_on = models.DateTimeField(null=True, blank=True)

    objects = ActiveManager()

    class Meta:
        verbose_name = 'Package History'
        verbose_name_plural = 'Package History'
        ordering = ['-created_on', '-expiry_date']

    @property
    def refresh_period_start_on(self) -> datetime:
        """Returns the start date of the refresh period."""
        return self.refresh_period_end_on - timedelta(
            days=self.package.refresh_period
        )

    @property
    def refresh_period_end_on(self) -> datetime:
        """Returns the end date of the curren   t cycle before the benchmark
        quota refreshes.
        """
        today = timezone.now()
        focus_date = self.created_on
        refresh_period = self.package.refresh_period

        while focus_date < today:
            focus_date += timedelta(days=refresh_period)

        return focus_date

    def __str__(self):
        fmt = '%Y-%m-%d'
        created_on = self.created_on.strftime(fmt)
        if self.expiry_date:
            expiry_date = self.expiry_date.strftime(fmt)
        else:
            expiry_date = 'None'
        return f'[{created_on}-{expiry_date}] {self.account}'

    @classmethod
    def new_package_history(cls, account: Account) -> 'PackageHistory':
        """Create a new package history for the given account."""
        package = account.package
        rec = cls.objects.create(
            account=account,
            package=package,
            price=package.price,
            expiry_date=account.expiry_date,
        )
        rec.save()
        return rec


class BillingAddress(models.Model):
    """Represents the billing address of an account."""
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postcode = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name='Postcode/Zip Code'
    )

    class Meta:
        verbose_name = 'Billing Address'
        verbose_name_plural = 'Billing Addresses'

    def __str__(self):
        return f'{self.account} - {self.street_address}'
