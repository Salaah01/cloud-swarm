from django.db import models
from django.contrib.auth.models import User
from packages import models as package_models


class Account(models.Model):
    """Represents a package associated with an account."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    package = models.ForeignKey(
        package_models.Package,
        on_delete=models.PROTECT,
    )
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.package}'

    @classmethod
    def new_free_account(cls, user: User):
        """Create a new free account for the given user."""
        return cls.objects.create(
            user=user,
            package=package_models.Package.objects.get(name='Free'),
        )


class PackageHistory(models.Model):
    """Represents the package history of an account."""
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    package = models.ForeignKey(
        package_models.Package,
        on_delete=models.PROTECT,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Package History'
        verbose_name_plural = 'Package History'
        ordering = ['-created_on', '-expiry_date']

    def __str__(self):
        fmt = '%Y-%m-%d'
        created_on = self.created_on.strftime(fmt)
        if self.expiry_date:
            expiry_date = self.expiry_date.strftime(fmt)
        else:
            expiry_date = 'None'
        return f'[{created_on}-{expiry_date}] {self.account}'
