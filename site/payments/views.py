import json
import stripe
from django.conf import settings
from django import http
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from . import models as stripeapp_models
from . import payment_intent

STRIPE_SETTINGS = settings.STRIPE
stripe.api_key = STRIPE_SETTINGS['secret_key']


def handle_payment(request: http.HttpRequest, content_type_id: int, object_id: int) -> http.HttpResponse:

    pay_intent_id = request.POST.get('pay-intent-id')
    model_info = stripeapp_models.ModelInfo(
        request.POST['app-name'],
        request.POST['model-name'],
        request.POST['object-id'],
        request.POST['content-id'],
        request.POST['amount-attr']
    )

    if not payment_intent.validate_payment(pay_intent_id, model_info):
        messages.error(request, 'An error occurred on taking your payment.')
        return http.HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    payment_hist = stripeapp_models.PaymentHistory.create_from_pay_intent(
        pay_intent_id=pay_intent_id,
        success=True,
        content_type_id=content_type_id,
        object_id=object_id,
    )
    # TODO: which signal to raise
    stripeapp_models.PAYMENT_SUCCESS.send(
        sender=type(payment_hist.object),
        instance=payment_hist.object,
        transaction_id=payment_hist.pay_intent_id,
        amount=payment_hist.amount
    )
    messages.success(request, 'Your payment has been successful.')

    return http.HttpResponseRedirect(request.POST['next'])


@csrf_exempt
def failed_payment(request) -> http.JsonResponse:
    """Stored failed payments."""

    # csrf check is turned off, so we will limit the information provided in
    # the response.
    data = json.loads(request.body)
    pay_intent_id = data.get('pay_intent_id')
    if not pay_intent_id:
        return http.JsonResponse({'success': False, 'error_code': 1})

    # Check if the pay intent even exists.
    try:
        payment_intent.get_intent(pay_intent_id)
    except stripe.error.InvalidRequestError:
        return http.JsonResponse({'success': False, 'error_code': 2})

    payment_hist = stripeapp_models.PaymentHistory.create_from_pay_intent(
        pay_intent_id,
        False,
        data['content_id'],
        data['object_id']
    )

    stripeapp_models.PAYMENT_FAILED.send(
        sender=type(payment_hist.object),
        instance=payment_hist.object,
        transaction_id=payment_hist.pay_intent_id,
        amount=payment_hist.amount
    )

    return http.JsonResponse({'success': True})
