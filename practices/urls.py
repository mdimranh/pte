from django.urls import include, path

urlpatterns = [
    path('practice/', include('practices.read_aloud.urls')),
    path('', include('practices.discussion.urls')),
    path('', include('practices.answer.urls')),
    path('', include('practices.summarize.urls')),
]