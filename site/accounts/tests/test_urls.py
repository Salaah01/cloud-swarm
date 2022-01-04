"""Unittests for the accounts URLs."""

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import change_password, login, profile, register


class TestUrls(SimpleTestCase):
    """Unittest to check that the urls resolve the correct view."""

    def test_change_password(self) -> None:
        """Tests that the change password URL resolves correctly."""
        self.assertEquals(
            resolve(reverse('change_password')).func,
            change_password
        )

    def test_login(self) -> None:
        """Tests that the login URL resolves correctly."""
        self.assertEquals(
            resolve(reverse('login')).func,
            login
        )

    def test_profile(self) -> None:
        """Tests that the profile URL resolves correctly."""
        self.assertEquals(
            resolve(reverse('profile')).func,
            profile
        )

    def test_register(self) -> None:
        """Tests that the register URL resolves correctly."""
        self.assertEquals(
            resolve(reverse('register')).func,
            register
        )
