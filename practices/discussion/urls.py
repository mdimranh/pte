from django.urls import path

from .views import DiscussionCreateView, DiscussionListView

urlpatterns = [
    path('read_aloud/discussions/<str:id>', DiscussionListView.as_view()),
    path('discussion', DiscussionCreateView.as_view())
]