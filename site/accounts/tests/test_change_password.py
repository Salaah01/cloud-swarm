"""Unittests for the change password view."""

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestViewsChangePassword(TestCase):
    """Unittests for the change password view."""

    def setUp(self):
        self.client = Client()

    def test_change_password(self):
        user = User.objects.create(username='test_user')
        user.set_password('test')
        user.save()
        self.client.login(username='test_user', password='test')
        self.client.post(
            reverse('change_password'),
            data={
                'old_password': 'test',
                'new_password1': 'abcdef12345',
                'new_password2': 'abcdef12345'
            }
        )
        self.client.logout()
        self.client.login(username='test_user', password='test'),
        self.assertIsNone(
            self.client.session.get('_auth_user_id'),
            'Old password still works.'
        )

        self.client.login(username='test_user', password='abcdef12345'),
        self.assertTrue(
            self.client.session.get('_auth_user_id'),
            'New password does not work.'
        )

        self.client.login(username='test_user', password='test')
