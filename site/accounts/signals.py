from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from . import models as accounts_models


@receiver(post_save, sender=User)
def create_account(sender, instance: User, created: bool, **kwargs):
    if created:
        accounts_models.Account.new_free_account(instance)
