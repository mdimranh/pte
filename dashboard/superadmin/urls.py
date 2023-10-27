from django.urls import path

from .views import *

urlpatterns = [
    path("superadmin/test/counts", TestStatisticsView.as_view())
]
