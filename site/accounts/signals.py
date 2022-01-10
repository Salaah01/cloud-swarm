from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from . import models as accounts_models


@receiver(post_save, sender=User)
def create_account(sender, instance: User, created: bool, **kwargs):
    if created:
        accounts_models.Account.new_free_account(instance)


def on_new_account_package(
    sender,
    instance: accounts_models.Account,
    **kwargs
):
    """Create a new package history record."""
    accounts_models.PackageHistory.new_package_history(instance)


accounts_models.NEW_ACCOUNT_PACKAGE.connect(
    on_new_account_package,
    accounts_models.Account,
)
