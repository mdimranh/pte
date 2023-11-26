from django.urls import include, path

urlpatterns = [
    path("", include("dashboard.superadmin.urls")),
    path("", include("dashboard.student.urls"))
]
