from django.contrib.auth import get_user_model

User = get_user_model()


class StripeAddressMixin:
    """Behaves as an adapter which injects methods to retrieve address fields
    from a model.

    Implementation involves overriding the the `STRIPE_ADDRESS_FIELDS`
    dictionary where the value against each key is the name of the field in the
    model which contains the respective data.
    """

    STRIPE_ADDRESS_FIELDS = {
        'line1': None,
        'line2': None,
        'city': None,
        'state': None,
        'postal_code': None,
        'country': None,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If all the fields are None, then raise an implementation error.
        if all(value is None for value in self.STRIPE_ADDRESS_FIELDS.values()):
            raise NotImplementedError(
                'STRIPE_ADDRESS_FIELDS must be overridden.'
            )

    def stripe_address_fields(self) -> dict:
        """Returns a dictionary of address fields for Stripe."""
        return {
            key: getattr(self, value)
            for key, value in self.STRIPE_ADDRESS_FIELDS.items()
            if value is not None
        }


class StripeCustomerMixin:
    """A model mixin to be added to the models which has access to the stripe
    customer. The stripe customer model be a model instance which is at least
    similar to the Django User model.

    Implementation:
        * If the `user` field is not set, then ensure that a `stripe_customer`
        method is defined which returns the user object.
        * Create a `get_stripe_address` method which returns a model instance
        which inherits from the `StripeAddressMixin` class. If this is not
        possible, then create the method but return `None`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self, 'get_stripe_address'):
            raise NotImplementedError(
                'The `get_stripe_address` method must be implemented.'
            )

    def stripe_customer(self) -> User:
        """Returns the user object associated with this model."""
        return self.user
