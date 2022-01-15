import typing as _t
from decimal import Decimal
from dataclasses import dataclass
from django.db import models
from django.contrib.contenttypes.models import ContentType
from . import stripe_api

# Abstract Models


class ContentTypeModel(models.Model):
    """An abstract base class for models that need to reference other models
    by their content type.
    """
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        related_name='+'
    )
    object_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def object(self) -> models.Model:
        if not hasattr(self, '_object'):
            obj = None
            try:
                obj = self.content_type.get_object_for_this_type(
                    pk=self.object_id
                )
            except models.ObjectDoesNotExist:
                pass
            self._object = obj
        return self._object

    @classmethod
    def get_for_instance(
        cls,
        instance: models.Model
    ) -> _t.Union['PaymentHistory', None]:
        """Retrieves the payment history record for a given instance if it
        exists.

        Args:
            instance (models.Model): The instance for which to retrieve the
                payment history record.
        """
        try:
            return cls.objects.get(
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.pk
            )
        except cls.DoesNotExist:
            return None


# Models
class PaymentHistory(ContentTypeModel):
    pay_intent_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_type = models.CharField(max_length=20)
    last_4_digits = models.CharField(max_length=4)
    exp_month = models.PositiveIntegerField(verbose_name='Expiry month')
    created_on = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Payment History'
        verbose_name_plural = 'Payment History'

    @classmethod
    def create_for_instance(
        cls,
        instance: models.Model,
        amount: Decimal
    ) -> 'PaymentHistory':
        """Creates a payment history record for a given instance.

        Args:
            instance (models.Model): The instance for which to create the
                payment history record.
            amount (Decimal): The amount of the payment.
        """
        rec = cls.objects.create(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            amount=amount
        )
        rec.save()
        return rec


class Product(ContentTypeModel):
    product_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Stripe Product ID'
    )


class Price(models.Model):

    price_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Stripe Price ID',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='prices'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recurring = models.BooleanField()

    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'

# Model Mixins


class PaymentRecordMixin:
    @property
    def payment_history(self) -> _t.Union['PaymentHistory', None]:
        """Retrieves the payment history record for a given instance if it
        exists.
        """
        return PaymentHistory.get_for_instance(self)


# Data Classes

@dataclass
class ModelInfo:
    app_name: str
    model_name: str
    object_id: int
    content_type_id: int
    amount_attr: str

    def get_object(self) -> models.Model:
        return ContentType.objects.get_for_id(
            self.content_type_id
        ).get_object_for_this_type(
            pk=self.object_id
        )

    def get_amount(self, as_integral: bool = False) -> _t.Union[Decimal, int]:
        """Returns the amount of the instance.
        Args:
            as_integral (bool): Whether to return the amount as an integer. If
                True, the amount will be multiplied by 100.
        """

        amount = getattr(self.get_object(), self.amount_attr)
        if as_integral:
            return int(amount * 100)
        return amount

    @property
    def product(self) -> Product:
        """Retrieves the product for a given instance, otherwise creates a
        new product.
        """

    @property
    def metadata(self) -> _t.Dict[str, str]:
        """Returns the metadata for a given instance to be used in the Stripe
        API.
        """
        return {
            'content_type_id': self.content_type_id,
            'object_id': self.object_id,
        }

    @classmethod
    def from_instance(
        cls,
        model: models.Model,
        amount_attr: str,
    ) -> 'ModelInfo':
        """Creates a ModelInfo object from a model instance.

        Args:
            model (models.Model): The model instance.
            amount_attr (str): The name of the attribute that contains the
                amount.
        """
        return ModelInfo(
            app_name=model._meta.app_label,
            model_name=model._meta.model_name,
            object_id=model.pk,
            content_type_id=ContentType.objects.get_for_model(model).pk,
            amount_attr=amount_attr,
        )
