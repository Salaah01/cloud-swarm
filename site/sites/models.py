import hashlib
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from dns import resolver


def gen_txt_record(domain: str, created_on: datetime) -> str:
    """Generate a TXT record for a domain.
    Args:
        domain (str): The domain name.
        created_on (datetime): The date the record was created.
    Returns:
        str: The TXT record.
    """
    code = hashlib.sha256(f'{domain}{created_on}'.encode('utf-8')).hexdigest()
    return f'web-horde-verification={code}'


class Site(models.Model):
    """Represents a registered site."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    domain = models.CharField(max_length=100)
    txt_record = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on', 'name']

    def __str__(self):
        return f'{self.name} ({self.domain})'

    def save(self, *args, **kwargs):
        # Generate the TXT record.
        if not self.txt_record:
            self.txt_record = gen_txt_record(self.domain, self.created_on)

        # Generate slug
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    @property
    def verified(self):
        """Check that the txt record exists in the DNS."""
        try:
            answers = resolver.query(self.domain, 'TXT')
            for record in answers:
                if record.strings[0] == self.txt_record.encode():
                    return True
        except resolver.NoAnswer:
            pass
        return False


class SiteAccess(models.Model):
    """Represents a table which contains sites, the users who have
    access to them and their authorisation.
    """

    class AuthLevels(models.IntegerChoices):
        """Represents the authorisation levels."""
        VIEW_ONLY = 0
        MANAGER = 1
        ADMIN = 2

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_level = models.IntegerField(choices=AuthLevels.choices)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on', 'site', 'user']
        verbose_name_plural = 'Site Accesses'

    def __str__(self):
        return f'{self.site} - {self.user} ({self.auth_level})'

    def user_has_admin_access(self):
        """Check if the user has admin access."""
        return self.auth_level == self.AuthLevels.ADMIN

    def user_has_manager_access(self):
        """Check if the user has manager access."""
        return self.auth_level in [
            self.AuthLevels.MANAGER,
            self.AuthLevels.ADMIN
        ]

    def user_has_view_access(self):
        """Check if the user has view access."""
        return self.auth_level in [
            self.AuthLevels.VIEW_ONLY,
            self.AuthLevels.MANAGER,
            self.AuthLevels.ADMIN
        ]
