"""Unittests for the login page."""
from django.test import LiveServerTestCase, TestCase, Client
from core_functions import selenium_browser, unittest_helpers
from django.urls import reverse


class TestLiveLogin(LiveServerTestCase):
    """Tests the login workflow using selenium."""

    def setUp(self):
        """Sets up the clients."""
        self.browser = selenium_browser()

    def tearDown(self):
        """Closes the browser."""
        self.browser.close()

    def _go_to_login_page(self):
        """Sends the user to the login page."""
        self.browser.get(self.live_server_url + reverse('login'))

    def test_incorrect_login(self):
        """Test that incorrect login details redirects the user back to the
        login page.
        """
        self._go_to_login_page()
        self.browser.find_element_by_name('email').send_keys('test@test.com')
        self.browser.find_element_by_name('password').send_keys('password')
        self.browser.find_element_by_id('register-submit').click()
        self.assertTrue('/accounts/login' in self.browser.current_url)


class TestLogin(TestCase):
    """Tests the login view."""
    USER_PASSWORD = 'password'

    @classmethod
    def setUpTestData(cls):
        unittest_helpers.get_user()

    def setUp(self):
        self.client = Client()
        self.user = unittest_helpers.get_user()
        self.user.set_password(self.USER_PASSWORD)
        self.user.save()

    def test_already_authenticated(self):
        """Test that an user that is already authenticated is redirected to
        index.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('login'), follow=True)
        self.assertEqual(response.redirect_chain[-1][0], '/')

    def test_valid_creds(self):
        """Test that the user is able to login with the correct credentials."""

        self.client.post(
            reverse('login'),
            data={'email': self.user.email, 'password': self.USER_PASSWORD}
        )

        self.assertTrue(
            self.client.session.get('_auth_user_id'),
            'User not logged in.'
        )

    def test_invalid_creds(self):
        """Test that if a user does not provide the correct credentials they
        are not logged in.
        """
        self.client.post(
            reverse('login'),
            data={'email': self.user.email, 'password': 'wrong_password'}
        )
        self.assertIsNone(
            self.client.session.get('_auth_user_id'),
            'User logged in with invalid credentials.'
        )

    def test_correct_user_logged_in(self):
        """Test that the user logs into the correct account."""

        unittest_helpers.get_user(100)

        self.client.post(
            reverse('login'),
            data={'email': self.user.email, 'password': self.USER_PASSWORD}
        )
        self.assertEquals(
            self.client.session.get('_auth_user_id'),
            str(self.user.id),
            'Logged into the wrong user account.'
        )

    def test_no_password(self):
        """Test the behaviour when when the password is not provided."""
        self.client.post(
            reverse('login'),
            data={'email': 'test@email.com'}
        )

        self.assertIsNone(
            self.client.session.get('_auth_user_id'),
            'Logged into without password.'
        )

    def test_no_email(self):
        """Test the behaviour when the email has not been provided."""
        self.client.post(
            reverse('login'),
            data={'password': 'test'}
        )
        self.assertIsNone(
            self.client.session.get('_auth_user_id'),
            'Logged into without email.'
        )
