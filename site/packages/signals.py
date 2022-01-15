from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from payments import stripe_api, models as payment_models
from . import models as package_models


DEFAULT_CURRENCY = settings.DEFAULT_CURRENCY


@receiver(post_save, sender=package_models.Package)
def create_product(
    sender,
    instance: package_models.Package,
    created: bool,
    **kwargs
):
    """Creates a new Stripe product and related price when a new product is
    created.
    """
    if not created:
        return

    model_info = payment_models.ModelInfo.from_instance(instance, 'price')
    stripe_product = stripe_api.Product.create(
        name=instance.name,
        metadata=model_info.metadata,
    )

    stripe_price = stripe_api.Price.create(
        product_id=stripe_product.id,
        unit_amount=model_info.get_amount(True),
        currency=DEFAULT_CURRENCY,
        recurring_interval=not instance.one_time_package and 'month' or None,
    )

    # Update the model with the stripe product and price IDs.
    package_models.Package.objects.filter(pk=instance.pk).update(
        stripe_product_id=stripe_product.id,
        stripe_price_id=stripe_price.id,
    )


def on_price_update(
    sender,
    instance: package_models.Package,
    **kwargs
):
    """When the price is updated, add a new price for this product and set
    to the price to use in the model.
    """
    # TODO: Handle subscriptions on the old price.
    model_info = payment_models.ModelInfo.from_instance(instance, 'price')
    stripe_price = stripe_api.Price.create(
        product_id=instance.stripe_product_id,
        unit_amount=model_info.get_amount(True),
        currency=DEFAULT_CURRENCY,
        recurring_interval=not instance.one_time_package and 'month' or None,
    )

    # Update the model with the stripe price ID.
    package_models.Package.objects.filter(pk=instance.pk).update(
        stripe_price_id=stripe_price.id,
    )


package_models.PACKAGE_PRICE_UPDATED.connect(
    on_price_update,
    package_models.Package
)
