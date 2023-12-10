from django.urls import include, path

from .views import *

urlpatterns = [
    path('student/plans', PlanView.as_view()),
    path('plans', PlanList.as_view()),
]