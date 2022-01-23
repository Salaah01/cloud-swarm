"""Unittests for the accounts views."""

from unittest import TestCase
from django.test import Client
from django.urls import reverse


class TestViews(TestCase):
    """Unittests for the accounts views."""

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

    def test_register(self) -> None:
        """Tests that the ``register`` view loads correctly."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
