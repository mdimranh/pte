from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from social_core.backends import google

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('accounts.urls')),
    path('practice/', include('practices.read_aloud.urls')),
    path('', include('practices.discussion.urls')),
    path('', include('practices.answer.urls')),
    path('api/token/', obtain_auth_token),  # DRF token authentication
    path('api/rest-auth/', include('dj_rest_auth.urls')),
    path('api/auth/', include('allauth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)