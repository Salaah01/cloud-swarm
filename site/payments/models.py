import typing as _t
from decimal import Decimal
from dataclasses import dataclass
from django.db import models
from django.contrib.contenttypes.models import ContentType


class PaymentHistory(models.Model):
    pay_intent_id = models.CharField(max_length=255, unique=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        related_name='+'
    )
    object_id = models.CharField(max_length=255, blank=True, null=True)
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


class PaymentRecordMixin:
    @property
    def payment_history(self) -> _t.Union['PaymentHistory', None]:
        """Retrieves the payment history record for a given instance if it
        exists.
        """
        return PaymentHistory.get_for_instance(self)


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

    def get_amount(self) -> Decimal:
        return getattr(self.get_object(), self.amount_attr)
