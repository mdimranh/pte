from django.urls import path

from .views import *

urlpatterns = [
    path('study_material/add', StudyMaterialCreateAPIView.as_view()),
    path('study_materials/<str:category>', StudyMaterialListAPIView.as_view()),
    path('study_material/<int:id>', StudyMaterialDestroyAPIView.as_view()),
    path("superadmin/test/counts", TestStatisticsView.as_view()),
    path("organization/add", OrgRegistrationView.as_view()),
    path("organizations", OrganizationListView.as_view()),
    path("organization/<int:id>/passwordchange", OrgPasswordChange.as_view()),
    path("adminuser/add", AdminUserAddView.as_view()),
    path("adminusers", AdminUserListView.as_view()),
    path("adminuser/<int:id>", DeleteAdminUserView.as_view())
]
