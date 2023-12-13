from django.urls import include, path

from .views import *

urlpatterns = [
    path('student/plans', PlanView.as_view()),
    path('plans', PlanList.as_view()),
    path('package/organization', OrganizationPackageCreateView.as_view()),
    path('package/organization/<id>', OrganizationPackageUpdateView.as_view()),
    path('package/organization/<id>/details', OrganizationPackageDetailsView.as_view()),
    path('packages/organization', OrganizationPackageListView.as_view()),
    path('package/student', StudentPackageCreateView.as_view()),
    path('package/student/<id>', StudentPackageUpdateView.as_view()),
    path('package/student/<id>/details', StudentPackageDetailsView.as_view()),
    path('packages/student', StudentPackageListView.as_view()),
]