import typing as _t
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts import models as account_models
from sites import models as site_models
from .. import forms as benchmark_forms

User = get_user_model()


def get_account(
    seed: int,
) -> account_models.Account:
    """Return a user with the given seed."""
    user = User.objects.get_or_create(
        username=f'User {seed}',
        password='password',
    )[0]
    return account_models.Account.objects.get(user=user)


def get_site(seed: int) -> site_models.Site:
    """Return a site with the given seed."""
    return site_models.Site.objects.get_or_create(
        name=f'Site {seed}',
        domain=f'example-{seed}.com',
        last_verified=timezone.now(),
    )[0]


class TestNewBenchmarkForm(TestCase):

    @staticmethod
    def sample_form(
        seed: int = 1,
        override: _t.Optional[dict] = None,
        num_requests: int = 1,
        num_servers: int = 1,
        account: _t.Optional[account_models.Account] = None,
    ) -> benchmark_forms.NewBenchmarkForm:
        """Returns a valid sample form object.
        Args:
            override (dict): A dictionary of values to override.
            seed (int): An integer value to allow the method to create specific
                sample forms.
            num_requests (int): The number of requests to create.
            num_servers (int): The number of servers to create.
            account (account_models.Account): The account to use.
        Returns:
            benchmark_forms.NewBenchmarkForm
        """
        site = get_site(seed)
        if not account:
            account = get_account(seed)
        site.add_account(account, site_models.SiteAccess.AuthLevels.ADMIN)
        package_history = account.package_history.first()
        package_history.package.quota = 100
        package_history.package.save()

        data = {
            'site': site,
            'num_requests': num_requests,
            'num_servers': num_servers,
        } | (override or {})

        form = benchmark_forms.NewBenchmarkForm(
            data=data,
            account=account,
            site=site
        )
        form.is_valid()
        return form

    def test_valid_form(self):
        """Test that the basic form data is valid."""
        form = self.sample_form()
        self.assertTrue(form.is_valid(), form.errors)

    def test_clean_site_admin(self):
        """Test that an admin of a site passes validation."""
        site = get_site(1)
        account = get_account(1)
        site.add_account(account, site_models.SiteAccess.AuthLevels.ADMIN)
        package_history = account.package_history.first()
        package_history.package.quota = 100
        package_history.package.save()

        form = self.sample_form(1, {'site': site})
        self.assertTrue(form.is_valid(), form.errors)

    def test_clean_site_manager(self):
        """Test that a manager of a site passes validation."""
        site = get_site(1)
        account = get_account(1)
        site.add_account(account, site_models.SiteAccess.AuthLevels.MANAGER)
        package_history = account.package_history.first()
        package_history.package.quota = 100
        package_history.package.save()

        form = self.sample_form(1, {'site': site})
        self.assertTrue(form.is_valid(), form.errors)

    def test_clean_site_view_only(self):
        """Test that an account with view only access on a site does not
        pass validation.
        """
        site = get_site(1)
        account = get_account(1)
        site.add_account(account, site_models.SiteAccess.AuthLevels.VIEW_ONLY)
        package_history = account.package_history.first()
        package_history.package.quota = 100
        package_history.package.save()

        form = self.sample_form(1, {'site': site})
        self.assertFalse(form.is_valid())

    def test_clean_site_wrong_site(self):
        """Test that an account that tries to run a benchmark on a site on
        which they do not have the right access are denied.
        """
        site_1 = get_site(1)
        site_2 = get_site(2)
        account_1 = get_account(1)
        account_2 = get_account(2)
        site_1.add_account(account_1, site_models.SiteAccess.AuthLevels.ADMIN)
        site_2.add_account(account_2, site_models.SiteAccess.AuthLevels.ADMIN)

        for account in (account_1, account_2):
            package_history = account.package_history.first()
            package_history.package.quota = 100
            package_history.package.save()

        form = self.sample_form(1, {'site': site_2})
        self.assertFalse(form.is_valid())

    def test_clean_site_non_existant_site(self):
        """Test that an account that tries to run a benchmark on a site that
        does not exist are denied.
        """
        account = get_account(1)
        package_history = account.package_history.first()
        package_history.package.quota = 100
        package_history.package.save()

        form = self.sample_form(1, {'site': site_models.Site.objects.create()})
        self.assertFalse(form.is_valid())

    def test_clean_account_insufficient_quote(self):
        """Test that an account that does not have  enough quote to run
        benchmarks fails the validation.
        """
        site = get_site(1)
        account = get_account(1)
        site.add_account(account, site_models.SiteAccess.AuthLevels.ADMIN)
        package_history = account.package_history.first()
        package_history.package.quota = 0
        package_history.package.save()

        form = self.sample_form(1, {'site': site})
        self.assertFalse(form.is_valid(), form.errors)

    def test_setup_site_fields(self):
        """Test that an account is only shown sites which they are allowed
        to benchmark.
        """
        site_1 = get_site(1)
        site_2 = get_site(2)
        site_3 = get_site(3)
        site_4 = get_site(4)
        account_1 = get_account(1)
        account_2 = get_account(2)
        site_1.add_account(account_1, site_models.SiteAccess.AuthLevels.ADMIN)
        site_2.add_account(
            account_1,
            site_models.SiteAccess.AuthLevels.MANAGER
        )
        site_3.add_account(
            account_1,
            site_models.SiteAccess.AuthLevels.VIEW_ONLY
        )
        site_4.add_account(
            account_2,
            site_models.SiteAccess.AuthLevels.ADMIN
        )

        form = benchmark_forms.NewBenchmarkForm(account=account_1)
        sites = form.fields['site'].queryset

        self.assertEqual(len(sites), 2, sites)
