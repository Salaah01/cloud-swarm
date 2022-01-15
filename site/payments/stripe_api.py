import typing as _t
import stripe
from django.conf import settings
from django.contrib.auth import get_user_model


STRIPE_PUBLISHABLE_KEY = settings.STRIPE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

User = get_user_model()


class Customer:
    """Class for managing Stripe customers.
    https://stripe.com/docs/api/customers
    """

    @classmethod
    def create(
        cls,
        user: User,
        address_fields: _t.Optional[_t.Dict[str, str]] = None
    ) -> stripe.Customer:
        """Crates a Stripe customer for the given user.
        Args:
            user - User object.
            address_fields - Dictionary of address fields.
        Returns:
            Stripe customer object.
        """
        return stripe.Customer.create(
            email=user.email,
            name=user.get_full_name(),
            address=address_fields or {}
        )

    @classmethod
    def retrieve(cls, customer_id: str) -> stripe.Customer:
        """Retrieves a Stripe customer for the given user.
        Args:
            customer_id - Stripe customer ID.
        Returns:
            Stripe customer object.
        """
        return stripe.Customer.retrieve(customer_id)

    @classmethod
    def update(
        cls,
        customer_id: str,
        user: User,
        address_fields: _t.Optional[_t.Dict[str, str]] = None,
    ) -> stripe.Customer:
        """Updates a Stripe customer for the given user.
        Args:
            customer_id - Stripe customer ID.
            user - User object.
            address_fields - Dictionary of address fields.
        Returns:
            Stripe customer object.
        """
        return stripe.Customer.modify(
            customer_id,
            address=address_fields or {},
            email=user.email,
            name=user.get_full_name(),
            metadata={
                'user_id': str(user.id),
                'username': user.username,
            }
        )

    @classmethod
    def delete(cls, customer_id: str) -> bool:
        """Deletes a Stripe customer for the given user.
        Args:
            customer_id - Stripe customer ID.
        Returns:
            True if successful, False otherwise.
        """
        result = stripe.Customer.delete(customer_id)
        return result.deleted

    @classmethod
    def list(cls, limit: int = 3) -> _t.List[stripe.Customer]:
        """Lists all Stripe customers.
        Args:
            limit - Number of customers to return.
        Returns:
            List of Stripe customer objects.
        """
        return stripe.Customer.list(limit=limit)


class Product:
    """Class for managing Stripe products.
    https://stripe.com/docs/api/products
    """

    @classmethod
    def create(
        cls,
        name: str,
        description: _t.Optional[str] = None,
        metadata: _t.Optional[_t.Dict[str, str]] = None
    ) -> stripe.Product:
        """Creates a Stripe product.
        Args:
            name - Product name.
            description - Product description.
            metadata - Dictionary of metadata.
        Returns:
            Stripe product object.
        """
        return stripe.Product.create(
            name=name,
            description=description,
            metadata=metadata or {}
        )

    @classmethod
    def retrieve(cls, product_id: str) -> stripe.Product:
        """Retrieves a Stripe product.
        Args:
            product_id - Stripe product ID.
        Returns:
            Stripe product object.
        """
        return stripe.Product.retrieve(product_id)

    @classmethod
    def update(cls, product_id: int, **kwargs) -> stripe.Product:
        """Updates a Stripe product.
        Args:
            product_id - Stripe product ID.
            **kwargs - Keyword arguments, these can be any of the following:
                name, description, metadata.
        Returns:
            Stripe product object.
        """
        return stripe.Product.modify(product_id, **kwargs)

    @classmethod
    def delete(cls, product_id: str) -> bool:
        """Deletes a Stripe product.
        Args:
            product_id - Stripe product ID.
        Returns:
            True if successful, False otherwise.
        """
        result = stripe.Product.delete(product_id)
        return result.deleted

    @classmethod
    def list(cls, limit: int = 3) -> _t.List[stripe.Product]:
        """Lists all Stripe products.
        Args:
            limit - Number of products to return.
        Returns:
            List of Stripe product objects.
        """
        return stripe.Product.list(limit=limit)


class Price:
    """Class for managing Stripe prices.
    https://stripe.com/docs/api/prices
    """

    @classmethod
    def create(
        cls,
        product_id: str,
        unit_amount: int,
        currency: str,
        metadata: _t.Optional[_t.Dict[str, str]] = None,
        recurring_interval: _t.Optional[str] = None,
    ) -> stripe.Price:
        """Creates a Stripe price.
        Args:
            product_id - Stripe product ID.
            unit_amount - Price in smallest denomination.
            currency - Currency code.
            metadata - Dictionary of metadata.
            recurring_interval - A string representing the frequency of the
                recurring price. Can be one of: 'day', 'week', 'month', 'year'.
        Returns:
            Stripe price object.
        """
        if recurring_interval:
            recurring = {
                'interval': recurring_interval,
                'interval_count': 1,
            }
        else:
            recurring = None
        return stripe.Price.create(
            product=product_id,
            unit_amount=unit_amount,
            currency=currency,
            metadata=metadata or {},
            recurring=recurring
        )

    @classmethod
    def retrieve(cls, price_id: str) -> stripe.Price:
        """Retrieves a Stripe price.
        Args:
            price_id - Stripe price ID.
        Returns:
            Stripe price object.
        """
        return stripe.Price.retrieve(price_id)

    @classmethod
    def update(cls, price_id: str, metadata: dict) -> stripe.Price:
        """Updates the metadata of a Stripe price.
        Args:
            price_id - Stripe price ID.
            metadata - Dictionary of metadata.
        Returns:
            Stripe price object.
        """
        return stripe.Price.modify(price_id, metadata=metadata)

    @classmethod
    def list(cls, limit=3) -> _t.List[stripe.Price]:
        """Lists all Stripe prices.
        Args:
            limit - Number of prices to return.
        Returns:
            List of Stripe price objects.
        """
        return stripe.Price.list(limit=limit)


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
