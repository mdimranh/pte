from django.urls import path

from .views import PlanView

urlpatterns = [
    path('plans', PlanView.as_view())
]