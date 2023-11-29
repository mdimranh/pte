from django.urls import path
from .views import *

urlpatterns = [
    path("payment", Payment.as_view()),
    path("payment/cancel", PaymentCancel.as_view())
]