from django.urls import path

from .views import *

urlpatterns = [
    path("student/add", RegistrationView.as_view()),
    path("students", StudenListView.as_view()),
    path("student/<int:pk>", StudenDetailsView.as_view()),
    path("plan/assign", AssignPlanView.as_view()),
    path("student/change_password", ChangePassword.as_view()),
]
