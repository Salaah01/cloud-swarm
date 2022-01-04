"""Unittest for the `SignUpInPostAction` class."""

from types import SimpleNamespace
from django.test import TestCase
from django.contrib.auth.models import User
from pages.models import Cities, Countries
from products.models import Listings, Statuses
from accounts.models import BillingAddresses, DeliveryAddresses
from sales.models import DeliveryOptions, Transactions, OrderStatuses
from accounts.views.functions.sign_up_in_post_action import SignUpInPostAction


class TestSignUpInPostAction(TestCase):
    """Unittest for the `SignUpInPostAction` class."""

    @classmethod
    def setUpTestData(cls):
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

    @staticmethod
    def user():
        """Returns the test user."""
        return User.objects.get(username='test@email.com')

    def setUp(self):
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

        user = User.objects.create(username='test@email.com')
        user.set_password('test')
        user.save()

        self.request = SimpleNamespace(
            session=SimpleNamespace(),
            user=SimpleNamespace(id=1)
        )

    def test_link_transaction(self):
        """Test the link transaction method links a user transaction correctly.
        """
        SignUpInPostAction._link_transaction(self.user(), 1)

        self.assertEqual(Transactions.objects.get(id=1).user, self.user())
        self.assertEqual(BillingAddresses.objects.get(id=1).user, self.user())
        self.assertEqual(DeliveryAddresses.objects.get(id=1).user, self.user())

    def test_link_transaction_invalid_email(self):
        """Test that transactions are not linked when the user's email does not
        match the email provided during billing.
        """
        user = self.user()
        user.username = 'test2@email.com'
        user.save()

        with self.assertRaises(Exception):
            SignUpInPostAction._link_transaction(
                User.objects.get(username='test2@email.com'),
                1
            )
