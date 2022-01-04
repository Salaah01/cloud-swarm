"""Unittests for the login API view."""

import json
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from pages.models import Cities, Countries
from products.models import Listings, Statuses
from accounts.models import BillingAddresses, DeliveryAddresses
from sales.models import DeliveryOptions, Transactions, OrderStatuses


class TestViewLoginAPI(TestCase):
    """Unittests for the login API view."""

    def setUp(self):
        self.client = Client()
        user = User.objects.create(username='test@email.com')
        user.set_password('test')
        user.save()

    def test_valid_creds(self):
        """Test that the user is able to login with the correct credentials."""
        self.client.post(
            reverse('login_api'),
            data=json.dumps({'email': 'test@email.com', 'password': 'test'}),
            content_type='application/json'
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
            reverse('login_api'),
            data=json.dumps(
                {'email': 'test@email.com', 'password': 'wrong_password'}
            ),
            content_type='application/json'
        )
        self.assertIsNone(
            self.client.session.get('_auth_user_id'),
            'User logged in with invalid credentials.'
        )

    def test_correct_user_logged_in(self):
        """Test that the user logs into the correct account."""
        User.objects.create(username='test2@email.com', password='test').save()
        userID = User.objects.get(username='test@email.com').id
        self.client.post(
            reverse('login_api'),
            data=json.dumps({'email': 'test@email.com', 'password': 'test'}),
            content_type='application/json'
        )
        self.client.login(username='test@email.com', password='test')
        self.assertEquals(
            self.client.session.get('_auth_user_id'),
            str(userID),
            'Logged into the wrong user account.'
        )

    def test_no_password(self):
        """Test the behaviour when when the password is not provided."""
        self.client.post(
            reverse('login_api'),
            data=json.dumps({'email': 'test@email.com'}),
            content_type='application/json'
        )

        self.assertIsNone(
            self.client.session.get('_auth_user_id'),
            'Logged into without password.'
        )

    def test_no_email(self):
        """Test the behaviour when the email has not been provided."""
        self.client.post(
            reverse('login_api'),
            data=json.dumps({'password': 'test'}),
            content_type='application/json'
        )
        self.assertIsNone(
            self.client.session.get('_auth_user_id'),
            'Logged into without email.'
        )

    def test_post_action_link_transaction(self):
        """Tests the link transaction post action."""

        # Test data
        Statuses.objects.get_or_create(name='Active')
        Listings.objects.create(
            id=1,
            name='listing',
            description='description',
            status=Statuses.objects.get(name='Active'),
            short_description='short desc',
            gross_price=1,
            vat=2,
            uri='listing'
        ).save()

        OrderStatuses.objects.get_or_create(name='Active')

        billingAddress = BillingAddresses.objects.create(
            id=1,
            user=None,
            first_name='first name',
            surname='surname',
            address_line_1='ad1',
            city=Cities.objects.get(name='London', country_code='GBR'),
            country=Countries.objects.get(country_code='GBR'),
            postcode='pc',
            email='test@email.com'
        )
        billingAddress.save()

        deliveryAddress = DeliveryAddresses.objects.create(
            id=1,
            user=None,
            first_name='first name',
            surname='surname',
            address_line_1='ad1',
            city=Cities.objects.get(name='London', country_code='GBR'),
            country=Countries.objects.get(country_code='GBR'),
            postcode='pc',
        )
        deliveryAddress.save()

        Transactions.objects.create(
            id=1,
            delivery_option=DeliveryOptions.objects.get(id=1),
            payment_id='abc',
            currency='GBP',
            amount=10,
            delivery_price=5,
            discount=0,
            delivery_address=deliveryAddress,
            billing_address=billingAddress,
            status=OrderStatuses.objects.get(name='Active')
        )

        self.client.post(
            reverse('login_api'),
            data=json.dumps({
                'email': 'test@email.com',
                'password': 'test',
                'postActions': ['link_transaction'],
                'postActionKwargs': '{"tid":1}'
            }),
            content_type='application/json'
        )

        user = User.objects.filter(username='test@email.com')
        if not user:
            self.fail('User was not created.')

        user = user[0]

        self.assertEqual(Transactions.objects.get(id=1).user, user)
        self.assertEqual(BillingAddresses.objects.get(id=1).user, user)
        self.assertEqual(DeliveryAddresses.objects.get(id=1).user, user)

    def test_get_request(self):
        """Test that a get request is rejected."""
        response = self.client.get(reverse('login_api'))
        self.assertIsNone(self.client.session.get('_auth_user_id'))
        self.assertFalse(
            json.loads(response.content)['success']
        )
