import typing as _t
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts import models as account_models
from .. import models as site_models, forms as site_forms

User = get_user_model()


class TestNewSiteForm(TestCase):

    @staticmethod
    def sample_form(
        override: _t.Optional[dict] = None,
        seed: int = 1,
    ) -> site_forms.NewSiteForm:
        """Return a sample form.
        Args:
            override (dict): A dictionary of values to override.
            seed (int): An integer value to allow the method to create specific
                sample forms.
        Returns:
            site_forms.NewSiteForm: The sample form.
        """
        user = User.objects.get_or_create(
            username=f'test-{seed}',
            password=f'test-{seed}'
        )[0]

        data = {
            'name': f'Example {seed}',
            'slug': f'example-{seed}',
            'domain': f'example-{seed}-site.com',
        } | (override or {})

        form = site_forms.NewSiteForm(
            data=data,
            account=account_models.Account.objects.get(user=user)
        )

        form.is_valid()
        return form

    def test_valid_form(self):
        """Test that the basic sample data provided is valid."""
        form = self.sample_form()
        self.assertTrue(form.is_valid(), form.errors)

    def test_clean_domain(self):
        """Test that the domain is cleaned properly."""
        form = self.sample_form({'domain': 'example.com'})
        self.assertTrue(form.is_valid(), form.errors)
        form = self.sample_form({'domain': 'example-com'})
        self.assertFalse(form.is_valid(), form.errors)

    def test_clean_prevents_duplicate_access(self):
        """Check that if an account already has access to a site, then the form
        raises an error.
        """
        user = User.objects.create_user(username='test', password='test')
        account = account_models.Account.objects.get(user=user)
        site = site_models.Site.objects.create(
            name='Example',
            slug='example',
            domain='example.com',
        )
        site.add_account(account, 0)
        form = site_forms.NewSiteForm(
            data={
                'name': 'Example',
                'slug': 'example',
                'domain': 'example.com',
            },
            account=account
        )
        self.assertFalse(form.is_valid(), form.errors)

    def test_site_already_exists(self):
        """Check that if a site already exists, then a new user can still
        submit a form with the site.
        """
        site_params = {
            'name': 'Example',
            'slug': 'example',
            'domain': 'example.com',
        }
        site_models.Site.objects.create(**site_params)
        form = self.sample_form(site_params)
        self.assertTrue(form.is_valid(), form.errors)

    def test_save(self):
        """On save, the form should add admin access to the site. Validate
        this behaviour.
        """
        self.sample_form().save()
        self.assertTrue(site_models.SiteAccess.objects.count(), 1)
