"""Unittests for the logout view."""

from django.test import TestCase, Client
from django.shortcuts import reverse
from core_functions import unittest_helpers


class TestLogout(TestCase):
    """Unittests for the logout view."""

    @classmethod
    def setUpTestData(cls):
        unittest_helpers.get_user()

    def setUp(self):
        self.client = Client()
        self.client.force_login(unittest_helpers.get_user())

    def test_logout(self):
        """Tests that the user is logged out successfully."""
        self.client.get(reverse('logout'), follow=True)
        self.assertIsNone(self.client.session.get('_auth_user_id'))

    def test_redirect_to_index(self):
        """When the referrer is not available should redirect to index."""
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.redirect_chain[-1][0], '/')

    def test_redirect_to_last_page(self):
        """Should redirect to the last page the user was on on logout."""
        response = self.client.get(
            reverse('logout'),
            follow=True,
            HTTP_REFERER='/privacy-policy/'
        )
        self.assertEqual(response.redirect_chain[-1][0], '/privacy-policy/')
