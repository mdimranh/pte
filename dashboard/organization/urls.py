from django.urls import path

from .views import *

urlpatterns = [
    path("student/add", RegistrationView.as_view()),
    path("students", StudenListView.as_view()),
    path("student/<int:pk>", StudenRetriveDestroyApiView.as_view()),
    path("student/<int:id>/changepassword", StudentPasswordChange.as_view()),
    path("student/<int:id>/update", StudentUpdateApiView.as_view()),
    path("plan/assign", AssignPlanView.as_view()),
    path("student/change_password", ChangePassword.as_view()),
    path("group", GroupCreateView.as_view()),
    path("groups", GroupListView.as_view()),
    path("exam_calender", ExamCalenderView.as_view()),
    path("student/counts", StudentDataCounts.as_view()),
    path("student/recentjoined", RecentJoinedStudentList.as_view()),
]
