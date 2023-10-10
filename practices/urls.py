from django.urls import include, path

urlpatterns = [
    # path('practice/', include('practices.read_aloud.urls')),
    path('', include('practices.discussion.urls')),
    path('', include('practices.answer.urls')),
    # path('', include('practices.summarize.urls')),
    path('', include('practices.highlight_summary.urls')),
    path('', include('practices.multi_choice.urls')),
    path('', include('practices.missing_word.urls')),
    path('', include('practices.dictation.urls')),
]