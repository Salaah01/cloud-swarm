from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts import models as account_models
from .. import models as site_models


User = get_user_model()


class TestBasicViews(TestCase):
    """Tests simple views that do not have any complex logic and mostly just
    render a template.
    """

    def test_dashboard(self):
        """Test that the dashboard view renders the correct template."""
        response = self.client.get(reverse('sites-dashboard'))
        self.assertTemplateUsed(response, 'sites/dashboard.html')
        self.assertEqual(response.status_code, 200)


class TestNewSiteView(TestCase):
    """Tests the new site view."""

    def setUp(self):
        # Create a user and log them in.
        self.user = User.objects.create_user(username='test', password='test')
        self.client = Client()
        self.client.login(username='test', password='test')
        self.account = account_models.Account.objects.get(user=self.user)

    def test_get_new_site(self):
        """Test that the new site view renders the correct template."""
        response = self.client.get(reverse('new_site'))
        self.assertTemplateUsed(response, 'sites/new_site.html')
        self.assertEqual(response.status_code, 200)

    def test_site(self):
        """Test that the site view renders the correct template."""
        site = site_models.Site.objects.create(
            name='Test Site',
            domain='iamsalaah.com',
        )
        site.add_account(self.account, 0)
        response = self.client.get(
            reverse('site', args=[site.id, site.slug])
        )
        self.assertTemplateUsed(response, 'sites/site.html')
        self.assertEqual(response.status_code, 200)
    def test_post_new_site(self):
        """Test that a new site can be created."""
        response = self.client.post(
            reverse('new_site'),
            {'name': 'Test Site', 'domain': 'iamsalaah.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(site_models.Site.objects.count(), 1)

    def test_post_bad_form(self):
        """Test that a bad form submission returns the correct template."""
        response = self.client.post(
            reverse('new_site'),
            {'name': 'Test Site'}
        )
        self.assertTemplateUsed(response, 'sites/new_site.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(site_models.Site.objects.count(), 0)
