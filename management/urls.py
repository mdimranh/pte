from django.urls import include, path

from .views import PlanView

urlpatterns = [
    path('plans', PlanView.as_view())
]