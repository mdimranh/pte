from django.urls import path
from .views import *

urlpatterns = [
    path("payment/organization", OrganizationPaymentView.as_view()),
    path("payment/success/<uid>/<pid>", PaymentSuccess),
    path("payment/cancel/<pid>", PaymentCancel),
    path("payment/fail/<pid>", PaymentFail),
    path("payment/<id>/details", PaymentDetails.as_view()),
]