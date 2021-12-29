import typing as _t
import hashlib
from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from dns import resolver


# Utilities
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


# Models
class Site(models.Model):
    """Represents a registered site."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    domain = models.CharField(max_length=100)
    txt_record = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_benchmarked = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['created_on', 'name']

    def __str__(self):
        return f'{self.name} ({self.domain})'

    def add_user(self, user: User, auth_level: int) -> 'SiteAccess':
        """Add a user to the site.
        Args:
            user (User): The user to add.
            auth_level (int): The authorization level.
        """
        site_access = SiteAccess.objects.create(
            site=self,
            user=user,
            auth_level=auth_level
        )
        site_access.save()
        return site_access

    def save(self, *args, **kwargs):
        # Generate the TXT record.
        if not self.txt_record:
            self.txt_record = gen_txt_record(self.domain, self.created_on)

        # Generate slug
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    @property
    def absolute_url(self) -> str:
        """Get the absolute URL for a site record."""
        return reverse('sites:site', args=[self.id, self.slug])

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

    @classmethod
    def for_id_slug(cls, id: int, slug: str) -> _t.Optional['Site']:
        """Get a site by its ID and slug."""
        try:
            return cls.objects.get(id=id, slug=slug)
        except cls.DoesNotExist:
            return None

    @classmethod
    def for_user(
        cls,
        user: User,
        auth_level: int = 0,
    ) -> models.QuerySet['Site']:
        """Get all sites for a user.
        Args:
            user (User): The user to get sites for.
            auth_level (int): The user's auth level.
        """
        if not user or not user.is_authenticated:
            return cls.objects.none()

        return cls.objects.filter(
            id__in=SiteAccess.objects.filter(
                user=user,
                auth_level__gte=auth_level,
            ).values_list('site_id', flat=True),
        )


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
        unique_together = ('site', 'user')

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

    @classmethod
    def user_access(
        cls,
        site: Site,
        user: User
    ) -> _t.Union['SiteAccess', None]:
        """Get the site access record for a user.
        Args:
            site (Site): The site to get access for.
            user (User): The user to get access for.
        """
        if not user or not user.is_authenticated:
            return None

        try:
            return cls.objects.get(
                site=site,
                user=user,
            )
        except cls.DoesNotExist:
            return None

    @classmethod
    def user_for_site_id_slug(
        cls,
        site_id: int,
        site_slug: str,
        user: User,
        auth_level: int = 0,
    ) -> _t.Union['SiteAccess', None]:
        """Get the site access record for a user.
        Args:
            site_id (int): The site ID.
            site_slug (str): The site slug.
            user (User): The user to get access for.
            auth_level (int): The user's auth level.
        """
        if not user or not user.is_authenticated:
            return None
        site = Site.for_id_slug(site_id, site_slug)
        if not site:
            return None
        return cls.user_access(site, user)
