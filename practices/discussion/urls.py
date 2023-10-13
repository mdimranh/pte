from django.urls import path

from .views import *

urlpatterns = [
    path('read_aloud/discussions/<str:id>', ReadAloudDiscussionListView.as_view()),
    path('highlight_summary/discussions/<str:id>', HighlightSummaryDiscussionListView.as_view()),
    path('summarize/discussions/<str:id>', SummarizeDiscussionListView.as_view()),
    path('multi_choice/discussions/<str:id>', MultiChoiceDiscussionListView.as_view()),
    path('missing_word/discussions/<str:id>', MissingWordDiscussionListView.as_view()),
    path('dictation/discussions/<str:id>', DictationDiscussionListView.as_view()),
    path('discussion', DiscussionCreateView.as_view()),
    path('<model>/discussion', DiscussionAdd.as_view()),
    path('discussion/<int:pk>/like/', LikeDiscussion.as_view()),
    path('discussion/<int:pk>', DiscussionDelete.as_view())
]