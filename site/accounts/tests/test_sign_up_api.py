"""Unittests for the sign up API view."""

import json
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from pages.models import Cities, Countries
from products.models import Listings, Statuses
from accounts.models import CommPrefs, BillingAddresses, DeliveryAddresses
from sales.models import DeliveryOptions, Transactions, OrderStatuses


class TestViewsSignUpAPI(TestCase):
    """Unittests for the register view."""

    def setUp(self):
        self.client = Client()

    def test_register_member(self):
        """Tests that users can be registered."""
        self.client.post(
            reverse('sign_up_api'),
            data=json.dumps({
                'firstName': 'first name',
                'lastName': 'last name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'confirmPassword': 'test12345!',
                'termsAccepted': 'on'

            }),
            content_type='application/json'
        )
        self.assertEquals(
            User.objects.filter(username='test@test.com').count(),
            1
        )

    def test_no_first_name(self):
        """Tests behaviour where the first name is not provided."""
        self.client.post(
            reverse('sign_up_api'),
            data=json.dumps({
                'lastName': 'last name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'confirmPassword': 'test12345!',
                'termsAccepted': 'on'
            }),
            content_type='application/json'
        )

        self.assertFalse(User.objects.filter(username='test@test.com').count())

    def test_no_last_name(self):
        """Tests behaviour where the last name is not provided."""
        self.client.post(
            reverse('sign_up_api'),
            data=json.dumps({
                'firstName': 'first name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'confirmPassword': 'test12345!',
                'termsAccepted': 'on'
            }),
            content_type='application/json'
        )

        self.assertFalse(User.objects.filter(username='test@test.com').count())

    def test_no_password(self):
        """Tests behaviour where the password is not provided."""
        self.client.post(
            reverse('sign_up_api'),
            data=json.dumps({
                'firstName': 'first name',
                'lastName': 'last_name',
                'email': 'test@test.com',
                'confirmPassword': 'test12345!',
                'termsAccepted': 'on'
            }),
            content_type='application/json'
        )

        self.assertFalse(User.objects.filter(username='test@test.com').count())

    def test_no_tc_accepted(self):
        """Tests that the user is not registered if the terms and conditions
        have not been accepted.
        """
        self.client.post(
            reverse('sign_up_api'),
            data=json.dumps({
                'firstName': 'first name',
                'lastName': 'last name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'confirmPassword': 'test12345!',
            }),
            content_type='application/json'
        )
        self.assertEquals(
            User.objects.filter(username='test@test.com').count(),
            0
        )

    def test_comm_prefs(self):
        """Tests that the communication preference columns are created
        correctly.
        """
        self.client.post(
            reverse('sign_up_api'),
            data=json.dumps({
                'firstName': 'first name',
                'lastName': 'last name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'confirmPassword': 'test12345!',
                'termsAccepted': 'on',
                'commPrefNews': True,
                'commPrefBlogs': True,
                'comPrefPromos': False
            }),
            content_type='application/json'
        )
        commPrefs = CommPrefs.objects.get(
            user=User.objects.get(username='test@test.com')
        )
        self.assertEquals(commPrefs.promotions, False)
        self.assertEquals(commPrefs.blogs, True)
        self.assertEquals(commPrefs.newsletters, True)

    def test_duplicate_user(self):
        """Tests the behaviour when a user tries to register twice."""
        postParams = json.dumps({
            'firstName': 'first name',
            'lastName': 'last name',
            'email': 'test@test.com',
            'password': 'test12345!',
            'confirmPassword': 'test12345!',
            'termsAccepted': 'on'

        })
        self.client.post(
            reverse('sign_up_api'),
            data=postParams,
            content_type='application/json'
        )
        response = self.client.post(
            reverse('sign_up_api'),
            data=postParams,
            content_type='application/json'
        ).content

        self.assertEquals(
            User.objects.filter(username='test@test.com').count(),
            1
        )
        response = json.loads(response)
        self.assertFalse(response['success'])
        self.assertEqual(response['error_type'], 'Email exists')

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
            email='test@test.com'
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
            reverse('sign_up_api'),
            data=json.dumps({
                'firstName': 'first name',
                'lastName': 'last name',
                'email': 'test@test.com',
                'password': 'test12345!',
                'confirmPassword': 'test12345!',
                'termsAccepted': 'on',
                'postActions': ['link_transaction'],
                'postActionKwargs': '{"tid":1}'

            }),
            content_type='application/json'
        )

        user = User.objects.filter(username='test@test.com')
        if not user:
            self.fail('User was not created.')

        user = user[0]

        self.assertEqual(Transactions.objects.get(id=1).user, user)
        self.assertEqual(BillingAddresses.objects.get(id=1).user, user)
        self.assertEqual(DeliveryAddresses.objects.get(id=1).user, user)

    def test_rejects_get_request(self):
        """Tests that the API rejects GET requests."""
        response = self.client.get(reverse('sign_up_api'))
        self.assertEqual(response.status_code, 405)
        content = json.loads(response.content)
        self.assertFalse(content['success'])
