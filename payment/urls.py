from django.urls import path

from payment.apps import PaymentConfig
from payment.views import PaymentListAPIView, PaymentCreateAPIView

app_name = PaymentConfig.name

urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
]