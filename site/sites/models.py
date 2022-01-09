import typing as _t
import hashlib
from datetime import datetime, timedelta
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from dns import resolver
from accounts import models as account_models


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

    def add_account(
        self,
        account: account_models.Account,
        auth_level: int
    ) -> 'SiteAccess':
        """Add an account to the site.
        Args:
            account (account_models.Account): The account to add.
            auth_level (int): The authorization level.
        """
        site_access = SiteAccess.objects.create(
            site=self,
            account=account,
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
    def for_account(
        cls,
        account: account_models.Account,
        auth_level: int = 0,
    ) -> models.QuerySet['Site']:
        """Get all sites for a account.
        Args:
            account (account_models.Account): The account.
            auth_level (int): The account's auth level.
        """
        if account is None:
            return cls.objects.none()

        return cls.objects.filter(
            id__in=SiteAccess.objects.filter(
                account=account,
                auth_level__gte=auth_level,
            ).values_list('site_id', flat=True),
        )


class SiteAccess(models.Model):
    """Represents a table which contains sites, the accounts who have
    access to them and their authorisation.
    """

    class AuthLevels(models.IntegerChoices):
        """Represents the authorisation levels."""
        VIEW_ONLY = 0
        MANAGER = 1
        ADMIN = 2

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    account = models.ForeignKey(
        account_models.Account,
        on_delete=models.CASCADE
    )
    auth_level = models.IntegerField(choices=AuthLevels.choices)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on', 'site', ]
        verbose_name_plural = 'Site Accesses'
        unique_together = ('site', 'account')

    def __str__(self):
        return f'{self.site} - {self.account} ({self.auth_level})'

    def account_has_admin_access(self):
        """Check if the account has admin access."""
        return self.auth_level == self.AuthLevels.ADMIN

    def account_has_manager_access(self):
        """Check if the account has manager access."""
        return self.auth_level in [
            self.AuthLevels.MANAGER,
            self.AuthLevels.ADMIN
        ]

    def account_has_view_access(self):
        """Check if the account has view access."""
        return self.auth_level in [
            self.AuthLevels.VIEW_ONLY,
            self.AuthLevels.MANAGER,
            self.AuthLevels.ADMIN
        ]

    def account_has_auth(self, auth_level: int) -> bool:
        """Check if the acc has the given auth level.
        Args:
            auth_level (int): The auth level to check.
        Returns:
            bool: True if the acc has the given auth level.
        """
        return self.auth_level >= auth_level

    @classmethod
    def account_access(
        cls,
        site: Site,
        account: account_models.Account
    ) -> _t.Union['SiteAccess', None]:
        """Get the site access record for an account.
        Args:
            site (Site): The site to get access for.
            account (account_models.Account): The account to get access for.
        """
        if account is None:
            return None

        try:
            return cls.objects.get(
                site=site,
                account=account,
            )
        except cls.DoesNotExist:
            return None


class VerificationCheckLog(models.Model):
    """A log of verification checks."""

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    account = models.ForeignKey(
        account_models.Account,
        on_delete=models.CASCADE
    )
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
    def add_log(
        cls,
        site: Site,
        account: account_models.Account
    ) -> 'VerificationCheckLog':
        """Add a verification check log.
        Args:
            site (Site): The site to check.
            account (account_models.Account): The account to check.
        """
        log = cls.objects.create(site=site, account=account)
        log.save()
        return log
