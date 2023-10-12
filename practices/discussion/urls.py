from django.urls import path

from .views import *

urlpatterns = [
    path('read_aloud/discussions/<str:id>', DiscussionListView.as_view()),
    path('discussion', DiscussionCreateView.as_view()),
    path('<model>/discussion', DiscussionAdd.as_view()),
    path('discussion/<id>/like/', LikeDiscussion.as_view()),
    path('discussion/<id>', DiscussionDestryView.as_view())
]