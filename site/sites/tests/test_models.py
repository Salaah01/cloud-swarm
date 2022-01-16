from datetime import timedelta
from django.test import TestCase
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts import models as account_models
from .. import models as site_models

User = get_user_model()


class TestUtilities(TestCase):
    def test_gen_txt_record(self):
        domain = 'example.com'
        created_on = timezone.now()
        self.assertIsInstance(
            site_models.gen_txt_record(domain, created_on),
            str
        )


class TestSite(TestCase):

    @staticmethod
    def get_site(seed: int = 1) -> site_models.Site:
        """Gets or creates a `Site` instance.
        Args:
            seed - An integer to seed the creation of the `Site`.
        Returns:
            site_models.Site: The `Site` instance.
        """
        return site_models.Site.objects.get_or_create(
            name=f'Site {seed}',
            slug=f'site-{seed}',
            domain=f'{seed}.example.com',
            txt_record=f'cloud-swarm-verification={seed}',
        )[0]

    def test__str__(self):
        self.assertIsInstance(str(self.get_site()), str)

    def test_add_account(self):
        """Test that an account can be added to a site."""
        user = User.objects.create(
            username='test',
            password='test',
        )
        site = self.get_site()
        site_access = site.add_account(
            account_models.Account.objects.get(user=user),
            1
        )

        self.assertIsInstance(site_access, site_models.SiteAccess)
        self.assertEqual(site_access.site, site)

    def test_save_create_txt_record(self):
        """Test that where an instanced is saved which is missing a TXT record,
        that TXT record is created by the `save` method.
        """
        site = site_models.Site.objects.create(
            name='Test Site',
            slug='test-site',
            domain='test.example.com',
        )
        site.save()
        self.assertIsNotNone(site.txt_record)

    def test_save_create_slug(self):
        """Test that where an instanced is saved which is missing a slug,
        that slug is created by the `save` method.
        """
        site = site_models.Site.objects.create(
            name='Test Site',
            domain='test.example.com',
            txt_record='cloud-swarm-verification=test',
        )
        site.save()
        self.assertIsNotNone(site.slug)

    def test_absolute_urL(self):
        """Test that the method returns a string."""
        self.assertIsInstance(self.get_site().absolute_url, str)

    def test_previously_verified(self):
        """Test that the method returns the correct boolean."""
        site = self.get_site()
        self.assertFalse(site.previously_verified)
        site.last_verified = timezone.now()
        self.assertTrue(site.previously_verified)

    def test_verified(self):
        """Test that the method returns the correct boolean."""
        site = self.get_site()
        self.assertFalse(site.verified)

        # Site has been verified longer than the allowed time.
        site.last_verified = timezone.now() - timedelta(
            seconds=settings.SITES_VERIFY_DURATION_SECS + 100
        )
        self.assertFalse(site.verified)

        # Site has been verified within the allowed time.
        site.last_verified = timezone.now() - timedelta(
            seconds=settings.SITES_VERIFY_DURATION_SECS - 100
        )

    def test_for_id_slug(self):
        """Test that the method is able to return the correct instance if it
        exists otherwise `None`.
        """
        site = self.get_site()
        self.assertEqual(
            site_models.Site.for_id_slug(site.id, site.slug),
            site
        )
        self.assertIsNone(
            site_models.Site.for_id_slug(site.id, 'does-not-exist')
        )

    def test_for_account(self):
        """Test that all sites becoming to an account are returned."""
        site_1 = self.get_site()
        site_2 = self.get_site(2)
        self.get_site(3)

        user = User.objects.create(
            username='test',
            password='test',
        )

        account = account_models.Account.objects.get(user=user)
        site_1.add_account(account, 0)
        site_2.add_account(account, 0)

        returned_sites = site_models.Site.for_account(account)

        self.assertEqual(len(returned_sites), 2)
        self.assertIn(site_1, returned_sites)
        self.assertIn(site_2, returned_sites)

    def test_for_account_with_auth(self):
        """Test that all accounts that have the right auth. to access a site
        are returned.
        """
        site_1 = self.get_site()
        site_2 = self.get_site(2)

        user = User.objects.create(
            username='test',
            password='test',
        )
        account = account_models.Account.objects.get(user=user)

        site_1.add_account(account, 0)
        site_2.add_account(account, 1)

        returned_sites = site_models.Site.for_account(account, 1)

        self.assertEqual(len(returned_sites), 1)
        self.assertEqual(returned_sites[0], site_2)


class TestSiteAccess(TestCase):

    @staticmethod
    def get_site_access(seed: int = 1) -> site_models.SiteAccess:
        """Gets or creates a `SiteAccess` instance.
        Args:
            seed - An integer to seed the creation of the `SiteAccess`.
        Returns:
            site_models.SiteAccess: The `SiteAccess` instance.
        """
        return site_models.SiteAccess.objects.get_or_create(
            site=site_models.Site.objects.get_or_create(
                name=f'Site {seed}',
                slug=f'site-{seed}',
                domain=f'{seed}.example.com',
                txt_record=f'cloud-swarm-verification={seed}',
            )[0],
            account=account_models.Account.objects.get_or_create(
                user=User.objects.create(
                    username='test',
                    password='test',
                )
            )[0],
            auth_level=0,
        )[0]

    def test__str__(self):
        self.assertIsInstance(str(self.get_site_access()), str)

    def test_account_has_admin_access(self):
        """Test that the method returns the correct boolean."""
        site_access = self.get_site_access()
        self.assertFalse(site_access.account_has_admin_access())
        site_access.auth_level = site_models.SiteAccess.AuthLevels.ADMIN
        self.assertTrue(site_access.account_has_admin_access())

    def test_account_has_manager_access(self):
        """Test that the method returns the correct boolean."""
        site_access = self.get_site_access()
        self.assertFalse(site_access.account_has_manager_access())
        site_access.auth_level = site_models.SiteAccess.AuthLevels.MANAGER
        self.assertTrue(site_access.account_has_manager_access())
        site_access.auth_level = site_models.SiteAccess.AuthLevels.ADMIN
        self.assertTrue(site_access.account_has_manager_access())

    def test_account_has_view_access(self):
        """Test that the method returns the correct boolean."""
        site_access = self.get_site_access()
        self.assertTrue(site_access.account_has_view_access())
        site_access.auth_level = site_models.SiteAccess.AuthLevels.MANAGER
        self.assertTrue(site_access.account_has_view_access())
        site_access.auth_level = site_models.SiteAccess.AuthLevels.ADMIN
        self.assertTrue(site_access.account_has_view_access())

    def test_account_has_auth(self):
        """Test that the method returns the correct boolen when checking that
        the account has the correct authorisation.
        """
        site_access = self.get_site_access()
        self.assertTrue(site_access.account_has_auth(0))
        self.assertFalse(site_access.account_has_auth(1))
        self.assertFalse(site_access.account_has_auth(2))
        site_access.auth_level = site_models.SiteAccess.AuthLevels.ADMIN
        self.assertTrue(site_access.account_has_auth(0))
        self.assertTrue(site_access.account_has_auth(1))
        self.assertTrue(site_access.account_has_auth(2))

    def test_account_access(self):
        """Test that the method returns the correct record if it exists."""
        user_1 = User.objects.create(username='test', password='test')
        user_2 = User.objects.create(username='test2', password='test2')

        account_1 = account_models.Account.objects.get(user=user_1)
        account_2 = account_models.Account.objects.get(user=user_2)

        site_1 = site_models.Site.objects.create(
            name='Site 1',
            slug='site-1',
            domain='1.example.com',
        )
        site_2 = site_models.Site.objects.create(
            name='Site 2',
            slug='site-2',
            domain='2.example.com',
        )

        # Grant access to account_1 to site_1 and grant account_2 access to
        # site_2.
        site_access_1 = site_models.SiteAccess.objects.create(
            site=site_1,
            account=account_1,
            auth_level=0,
        )
        site_access_2 = site_models.SiteAccess.objects.create(
            site=site_2,
            account=account_2,
            auth_level=0,
        )

        # Check that the correct access records are returned.
        self.assertEqual(
            site_models.SiteAccess.account_access(site_1, account_1),
            site_access_1
        )
        self.assertIsNone(
            site_models.SiteAccess.account_access(site_1, account_2)
        )
        self.assertIsNone(
            site_models.SiteAccess.account_access(site_2, account_1)
        )
        self.assertEqual(
            site_models.SiteAccess.account_access(site_2, account_2),
            site_access_2
        )


class TestVerificationCheckLog(TestCase):

    @staticmethod
    def get_site(seed: int = 1) -> site_models.Site:
        """Gets or creates a `Site` instance.
        Args:
            seed - An integer to seed the creation of the `Site`.
        Returns:
            site_models.Site: The `Site` instance.
        """
        return site_models.Site.objects.get_or_create(
            name=f'Site {seed}',
            slug=f'site-{seed}',
            domain=f'{seed}.example.com',
            txt_record=f'cloud-swarm-verification={seed}',
        )[0]

    @staticmethod
    def get_account(seed: int = 1) -> account_models.Account:
        """Gets or creates an `Account` instance.
        Args:
            seed - An integer to seed the creation of the `Account`.
        Returns:
            account_models.Account: The `Account` instance.
        """
        return account_models.Account.objects.get_or_create(
            user=User.objects.create(
                username=f'test-{seed}',
                password='test',
            )
        )[0]

    def get_verification_check_log(
        self,
        seed: int = 1
    ) -> site_models.VerificationCheckLog:
        """Gets or creates a `VerificationCheckLog` instance.
        Args:
            seed - An integer to seed the creation of the
                `VerificationCheckLog`.
        Returns:
            site_models.VerificationCheckLog: The `VerificationCheckLog`
                instance.
        """
        return site_models.VerificationCheckLog.objects.get_or_create(
            site=self.get_site(seed),
            account=self.get_account(seed),
        )[0]

    def test__str__(self):
        self.assertIsInstance(str(self.get_verification_check_log()), str)

    def test_can_run_check(self):
        """Test that the method returns the correct boolean."""
        site = self.get_site()
        self.assertTrue(site_models.VerificationCheckLog.can_run_check(site))

        site_models.VerificationCheckLog.objects.create(
            site=site,
            account=self.get_account(),
        )
        self.assertFalse(site_models.VerificationCheckLog.can_run_check(site))

    def test_add_log(self):
        """Test that the method adds a log to the database."""
        site = self.get_site()
        account = self.get_account()

        site_models.VerificationCheckLog.add_log(site, account)

        log = site_models.VerificationCheckLog.objects.get(
            site=site,
            account=account,
        )
        self.assertIsInstance(log, site_models.VerificationCheckLog)
        self.assertEqual(
            site_models.VerificationCheckLog.objects.count(),
            1
        )
