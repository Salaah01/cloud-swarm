import typing as _t
import hashlib
from datetime import datetime, timedelta
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
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
    return f'cloud-swarm-verification={code}'


# Models
class Site(models.Model):
    """Represents a registered site."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    domain = models.CharField(max_length=100)
    txt_record = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_benchmarked = models.DateTimeField(blank=True, null=True)
    last_verified = models.DateTimeField(blank=True, null=True)

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
    def previously_verified(self) -> bool:
        """Whether the site was verified previously."""
        return self.last_verified is not None

    @property
    def verified(self) -> bool:
        """Check if the site is verified respecting the validation expiration
        time.
        """
        if self.last_verified is None:
            return False
        return self.last_verified > timezone.now() - timedelta(
            hours=settings.SITES_VERIFY_DURATION_SECS
        )

    def verify(self, force: bool = False) -> bool:
        """Verify a site.
        Args:
            force (bool): Force verification.
        Returns:
            bool: Whether the verification was successful.
        """
        if not force and self.verified:
            return True
        try:
            answers = resolver.query(self.domain, 'TXT')
            for record in answers:
                if record.strings[0] == self.txt_record.encode():
                    self.last_verified = timezone.now()
                    self.save()
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

    def user_has_auth(self, auth_level: int) -> bool:
        """Check if the user has the given auth level.
        Args:
            auth_level (int): The auth level to check.
        Returns:
            bool: True if the user has the given auth level.
        """
        return self.auth_level >= auth_level

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


class VerificationCheckLog(models.Model):
    """A log of verification checks."""

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{self.site} - {self.created_on}'

    @classmethod
    def can_run_check(cls, site: Site) -> bool:
        """Check if a verification check can run. This is to prevent a site
        from being checked too frequently.
        Args:
            site (Site): The site to check.
        Returns:
            bool: True if the check can run.
        """

        return not cls.objects.filter(
            site=site,
            created_on__gte=(
                timezone.now()
                - timedelta(seconds=settings.SITES_VERIFY_TIMEOUT_SECS)
            )
        ).exists()

    @classmethod
    def add_log(cls, site: Site, user: User) -> 'VerificationCheckLog':
        """Add a verification check log.
        Args:
            site (Site): The site to check.
            user (User): The user to check.
        """
        log = cls.objects.create(
            site=site,
            user=user,
        )
        log.save()
        return log
