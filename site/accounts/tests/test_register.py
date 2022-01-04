"""Unittests for the register view."""

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core_functions import unittest_helpers


class TestViewsRegister(TestCase):
    """Unittests for the register view."""

    def setUp(self):
        self.client = Client()

    def test_register_member(self):
        """Tests that users can be registered."""
        self.client.post(
            reverse('register'),
            data={
                'first-name': 'first name',
                'last-name': 'last name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'password-confirm': 'test12345!',
                'termsAccepted': 'on'

            }
        )
        self.assertEquals(
            User.objects.filter(username='test@test.com').count(),
            1
        )

    def test_no_first_name(self):
        """Tests behaviour where the first name is not provided."""
        self.client.post(
            reverse('register'),
            data={
                'last-name': 'last name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'password-confirm': 'test12345!',
                'termsAccepted': 'on'
            }
        )

        self.assertFalse(User.objects.filter(username='test@test.com').count())

    def test_no_last_name(self):
        """Tests behaviour where the last name is not provided."""
        self.client.post(
            reverse('register'),
            data={
                'first-name': 'first name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'password-confirm': 'test12345!',
                'termsAccepted': 'on'
            }
        )

        self.assertFalse(User.objects.filter(username='test@test.com').count())

    def test_no_password(self):
        """Tests behaviour where the password is not provided."""
        self.client.post(
            reverse('register'),
            data={
                'first-name': 'first name',
                'last-name': 'last_name',
                'email': 'test@test.com',
                'password-confirm': 'test12345!',
                'termsAccepted': 'on'
            }
        )

        self.assertFalse(User.objects.filter(username='test@test.com').count())

    def test_no_tc_accepted(self):
        """Tests that the user is not registered if the terms and conditions
        have not been accepted.
        """
        self.client.post(
            reverse('register'),
            data={
                'first-name': 'first name',
                'last-name': 'last name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'password-confirm': 'test12345!',

            }
        )
        self.assertEquals(
            User.objects.filter(username='test@test.com').count(),
            0
        )

    def test_already_authenticated(self):
        """Test that an user that is already authenticated is redirected to
        index.
        """
        self.client.force_login(unittest_helpers.get_user())
        response = self.client.get(reverse('register'), follow=True)
        self.assertEqual(response.redirect_chain[-1][0], '/')

    def test_email_exists(self):
        """Test that where an email is already in use, registration with that
        email fails.
        """
        self.client.post(
            reverse('register'),
            data={
                'first-name': 'first name',
                'last-name': 'last name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'password-confirm': 'test12345!',
                'termsAccepted': 'on'

            }
        )
        self.client.post(
            reverse('register'),
            data={
                'first-name': 'first name 2',
                'last-name': 'last name 2',
                'email': 'test@test.com',
                'password': 'test12345! 2',
                'password-confirm': 'test12345! 2',
                'termsAccepted': 'on'

            }
        )
        self.assertEquals(
            User.objects.filter(username='test@test.com').count(),
            1
        )
