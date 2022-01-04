"""Unittests for the accounts.utils module."""

from django.test import TestCase
from django.contrib.auth import models as auth_models
from django.shortcuts import reverse
from core_functions import unittest_helpers
from accounts import utils


class TestValidateEmail(TestCase):
    """Unittests for the validate_email function."""

    def test_valid_email(self):
        """Test that a valid email passes validation."""
        self.assertTrue(utils.validate_email('test@test.com'))

    def test_invalid_email(self):
        """Test that an invalid email fails validation."""
        self.assertFalse(utils.validate_email('test'))


class TestLoginUser(TestCase):
    """Unittests for the login_user function."""

    def setUp(self):
        """Setup the tests."""
        self.user = auth_models.User.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='password'
        )

    def test_invalid_email(self):
        """Test that an invalid email fails validation."""
        self.assertIsNone(utils.login_user(
            unittest_helpers.simple_get_response(),
            'test',
            'password'
        ))

    def test_valid_login(self):
        """Test that a valid login passes validation."""
        self.assertIsNotNone(utils.login_user(
            unittest_helpers.simple_get_response().wsgi_request,
            'test@test.com',
            'password'
        ))

    def test_invalid_login(self):
        """Test that an invalid login fails validation."""
        self.assertIsNone(utils.login_user(
            unittest_helpers.simple_get_response(),
            'test@test.com',
            'password2'
        ))


class TestValidatePassword(TestCase):
    """Unittests for the validate_password function."""

    def test_valid_password(self):
        """Test that a valid password passes validation."""
        self.assertTrue(utils.validate_password('passworddlfksdkfjds')[0])

    def test_invalid_password(self):
        """Test that an invalid password fails validation."""
        self.assertFalse(utils.validate_password('11111')[0])


class TestSignUpUser(TestCase):
    """Unittests for the sign_up_user function."""

    def test_invalid_email(self):
        """Test that an invalid email fails validation."""
        result = utils.sign_up_user(
            unittest_helpers.simple_get_response(),
            'test',
            'first name',
            'last name',
            'password',
            'password'
        )
        self.assertFalse(result.success)
        self.assertEqual(result.error_type, 'Invalid email')

    def test_duplicate_email(self):
        """Test that a duplicate email fails validation."""
        user = unittest_helpers.get_user()
        result = utils.sign_up_user(
            unittest_helpers.simple_get_response().wsgi_request,
            user.email,
            user.first_name,
            user.last_name,
            user.password,
            user.password
        )
        self.assertFalse(result.success)
        self.assertEqual(result.error_type, 'Email exists')

    def test_missing_field(self):
        """Test that a missing field fails validation."""
        result = utils.sign_up_user(
            unittest_helpers.simple_get_response().wsgi_request,
            'test@test.com',
            None,
            'last_name',
            'password',
            'password'
        )
        self.assertFalse(result.success)
        self.assertEqual(result.error_type, 'Missing field(s)')

    def test_password_not_matching(self):
        """Test that the validation checking the passord is equal to confirm
        password works.
        """
        result = utils.sign_up_user(
            unittest_helpers.simple_get_response().wsgi_request,
            'test@test.com',
            'first name',
            'last name',
            'password',
            'password2'
        )
        self.assertFalse(result.success)
        self.assertEqual(result.error_type, 'Passwords do not match')

    def test_valid_sign_up(self):
        """Test that a valid sign up passes validation."""
        result = utils.sign_up_user(
            unittest_helpers.simple_get_response().wsgi_request,
            'test@test.com',
            'first name',
            'last name',
            'password123',
            'password123'
        )
        self.assertTrue(result.success)
        self.assertIsNotNone(result.retuned_object)
