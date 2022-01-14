import typing as _t
import stripe
from django.conf import settings
from django.contrib.auth import get_user_model


STRIPE_PUBLISHABLE_KEY = settings.STRIPE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_customer(
    email: str,
    metadata: _t.Optional[dict] = None
) -> stripe.Customer:
    """Creates a Stripe customer object.
    Args:
        email: The email address of the customer.
        metadata: A dictionary of metadata to store with the customer.
    Returns:
        A stripe.Customer object.
    """
    return stripe.Customer.create(
        email=email,
        metadata=metadata or {}
    )


def create_subscription(
    customer_id: str,
    price_id: str
) -> stripe.Subscription:
    """Creates a Stripe subscription object.
    Args:
        customer_id: The ID of the customer to subscribe.
        price_id: The ID of the price to subscribe to.
    Returns:
        A stripe.Subscription object.
    """
    return stripe.Subscription.create(
        customer=customer_id,
        items=[{'price': price_id}],
        payment_behavior='default_incomplete',
        expand=['latest_invoice.payment_intent'],
    )
