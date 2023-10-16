from django.urls import path

from .views import *

urlpatterns = [
    path('read_aloud/<str:id>/discussions', ReadAloudDiscussionListView.as_view()),
    path('highlight_summary/<str:id>/discussions', HighlightSummaryDiscussionListView.as_view()),
    path('summarize/<str:id>/discussions', SummarizeDiscussionListView.as_view()),
    path('multi_choice/<str:id>/discussions', MultiChoiceDiscussionListView.as_view()),
    path('missing_word/<str:id>/discussions', MissingWordDiscussionListView.as_view()),
    path('dictation/<str:id>/discussions', DictationDiscussionListView.as_view()),
    path('discussion', DiscussionCreateView.as_view()),
    path('<model>/discussion', DiscussionAdd.as_view()),
    path('discussion/<int:pk>/like/', LikeDiscussion.as_view()),
    path('discussion/<int:pk>', DiscussionDelete.as_view())
]