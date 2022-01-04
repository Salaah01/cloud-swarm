"""Unittests for the `update_comm_prefs_api` view."""

import json
from django.test import Client, TestCase
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from core_functions import fetch_config
from accounts.models import CommPrefs

commPrefKeys = fetch_config('sales')['comm_pref_keys']


class TestViewUpdateCommPrefsAPI(TestCase):
    """Unittests for the `update_comm_prefs_api` view."""

    def send_post_req(self, data: dict) -> HttpResponse:
        """Sends a post request to the API.

        Args:
            data - (dict) Data to send in the post request.
        """

        return self.client.post(
            reverse('update_comm_prefs_api'),
            data=json.dumps(data),
            content_type='application/json'
        )

    def login(self) -> None:
        """Logs in as the test user."""
        self.client.login(username='test@email.com', password='test')

    @staticmethod
    def fetch_comm_prefs() -> CommPrefs:
        """Returns the test user's comm prefs (reruns the query again)."""
        return CommPrefs.objects.get(
            user=User.objects.get(username='test@email.com')
        )

    def set_all_pref_true(self) -> None:
        """Sets all the user preferences for the test user to True."""
        commPrefs = self.fetch_comm_prefs()
        commPrefs.newsletters = True
        commPrefs.blogs = True
        commPrefs.promotions = True
        commPrefs.save()

    def setUp(self):
        self.client = Client()
        user = User.objects.create(username='test@email.com')
        user.set_password('test')
        user.save()

        CommPrefs.objects.create(user=user).save()

    def test_set_newsletters_true(self):
        """Test that the newsletters preference can be set to true."""
        self.login()
        self.send_post_req({
            commPrefKeys['newsletters']: True,
        })

        self.assertTrue(self.fetch_comm_prefs().newsletters)
        self.assertFalse(self.fetch_comm_prefs().promotions)
        self.assertFalse(self.fetch_comm_prefs().blogs)

    def test_set_blogs_true(self):
        """Test that the blogs preference can be set to true."""
        self.login()
        self.send_post_req({
            commPrefKeys['blogs']: True,
        })

        self.assertTrue(self.fetch_comm_prefs().blogs)
        self.assertFalse(self.fetch_comm_prefs().promotions)
        self.assertFalse(self.fetch_comm_prefs().newsletters)

    def test_set_promotions_true(self):
        """Test that the promotions preference can be set to true."""
        self.login()
        self.send_post_req({
            commPrefKeys['promotions']: True,
        })

        self.assertTrue(self.fetch_comm_prefs().promotions)
        self.assertFalse(self.fetch_comm_prefs().newsletters)
        self.assertFalse(self.fetch_comm_prefs().blogs)

    def test_set_newsletters_false(self):
        """Test that the newsletters preference can be set false."""
        self.login()
        self.set_all_pref_true()
        self.send_post_req({
            commPrefKeys['newsletters']: False,
        })

        self.assertFalse(self.fetch_comm_prefs().newsletters)
        self.assertTrue(self.fetch_comm_prefs().blogs)
        self.assertTrue(self.fetch_comm_prefs().promotions)

    def test_set_blogs_false(self):
        """Test that the blogs preference can be set false."""
        self.login()
        self.set_all_pref_true()
        self.send_post_req({
            commPrefKeys['blogs']: False,
        })

        self.assertTrue(self.fetch_comm_prefs().newsletters)
        self.assertFalse(self.fetch_comm_prefs().blogs)
        self.assertTrue(self.fetch_comm_prefs().promotions)

    def test_set_promotions_false(self):
        """Test that the promotions preference can be set false."""
        self.login()
        self.set_all_pref_true()
        self.send_post_req({
            commPrefKeys['promotions']: False,
        })

        self.assertTrue(self.fetch_comm_prefs().newsletters)
        self.assertTrue(self.fetch_comm_prefs().blogs)
        self.assertFalse(self.fetch_comm_prefs().promotions)

    def test_user_with_no_prefs(self):
        """Test a row is created for a user that has not previously set
        communication preferences.
        """
        user = User.objects.create(username='newuser@email.com')
        user.set_password('test')
        user.save()
        self.client.login(username='newuser@email.com', password='test')
        self.send_post_req({
            commPrefKeys['newsletters']: True
        })

        commPrefs = CommPrefs.objects.get(
            user=User.objects.get(username='newuser@email.com')
        )

        self.assertTrue(commPrefs.newsletters)
        self.assertFalse(commPrefs.blogs)
        self.assertFalse(commPrefs.promotions)

    def test_get_request(self):
        """Test that a get request is rejected."""
        response = self.client.get(reverse('update_comm_prefs_api'))
        self.assertEqual(response.status_code, 405)
        self.assertFalse(json.loads(response.content)['success'])

    def test_unauthenticated(self):
        """Test that an authenticated user fails running any updates."""
        response = self.send_post_req({
            commPrefKeys['newsletters']: True,
        })
        self.assertEqual(response.status_code, 401)
        self.assertFalse(json.loads(response.content)['success'])
