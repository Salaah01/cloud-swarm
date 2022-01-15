import decimal
import json
import stripe

from django import template
from django.db import models
from django.conf import settings

from .. import stripe_api, models as payment_models

from ..forms import PaymentForm


# STRIPE_SETTINGS = settings.STRIPE
# stripe.api_key = STRIPE_SETTINGS['secret_key']
stripe_pub_key = settings.STRIPE_PUBLISHABLE_KEY

register = template.Library()


@register.inclusion_tag('payments/tags/subscription-form.html')
def render_subscription_form(
    instance: models.Model,
    amount_attr: str = 'amount',
    metadata: str = '{}',
):
    subscription = stripe_api.create_subscription(
        'cus_KxXgPaS9dB1GdK',
        'price_1KHcVIGndaflc50AxSSAInLC'
    )

    model_info = payment_models.ModelInfo.from_instance(instance, amount_attr)

    if model_info.get_amount() == 0:
        raise ValueError('Amount must be greater than 0.')

    return {
        'pay_intent_id': subscription.id,
        'client_secret': subscription.latest_invoice.payment_intent.client_secret,
        'stripe_pub_key': stripe_pub_key,
        'payment_form': PaymentForm(),
    }
