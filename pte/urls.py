from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('accounts.urls')),
    path('practice/', include('practices.read_aloud.urls')),
    path('', include('practices.discussion.urls')),
    path('', include('practices.answer.urls')),
    path('api/token/', obtain_auth_token),  # DRF token authentication
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)