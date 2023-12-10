from django.urls import path
from .views import *

urlpatterns = [
    path("payment", PaymentView.as_view()),
    path("payment/success/<uid>/<pid>", PaymentSuccess),
    path("payment/cancel/<pid>", PaymentCancel),
    path("payment/fail/<pid>", PaymentFail)
]