from django.urls import path
from . import views

urlpatterns = [
    path('subscription-webhook/', views.handle_subscription_callback),
    path('sample-payment/', views.SamplePayment.as_view()),
]
