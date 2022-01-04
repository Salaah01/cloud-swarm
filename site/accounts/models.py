"""Models relating to the user accounts."""

from typing import Optional
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# class CommPrefs(models.Model):
#     """User communication preferences."""
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     promotions = models.BooleanField(default=False)
#     blogs = models.BooleanField(default=False)
#     newsletters = models.BooleanField(default=False)
#     terms_last_agreed = models.DateTimeField(
#         null=True,
#         blank=True,
#         default=timezone.now
#     )

#     class Meta:
#         verbose_name_plural = 'Communication Preferences'
