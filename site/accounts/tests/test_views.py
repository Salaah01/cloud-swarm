"""Unittests for the accounts views."""

from unittest import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Statuses


class TestViews(TestCase):
    """Unittests for the accounts views."""

    @classmethod
    def setUpTestData(cls) -> None:
        Statuses.objects.get_or_create(name='Active')

    def setUp(self) -> None:
        self.client = Client()

    def test_change_password(self) -> None:
        """Tests that the ``ChangePassword`` view loads correctly."""
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 200)

    def test_login(self) -> None:
        """Tests that the ``login`` view loads correctly."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_profile_redirect(self) -> None:
        """Tests that the ``profile`` view redirects when user is not
        authenticated."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile(self) -> None:
        """Tests that the ``profile`` view loads correctly."""
        user = User.objects.create(username='testuser')
        user.set_password('test')
        user.save()
        self.client.login(username='testuser', password='test')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_register(self) -> None:
        """Tests that the ``register`` view loads correctly."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
