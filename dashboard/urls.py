from django.urls import include, path

urlpatterns = [
    path("", include("dashboard.superadmin.urls"))
]
