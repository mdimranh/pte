from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from dashboard.organization.urls import urlpatterns as org_urls
from dashboard.superadmin.urls import urlpatterns as sadmin_urls

from accounts.views import GetRoleApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('accounts.urls')),
    path('', include('practices.urls')),
    path('', include('management.urls')),
    path('', include('dashboard.urls')),
    path('', include('mocktest.urls')),
    path('', include('payment.urls')),
    path('user/role', GetRoleApi.as_view()),
    path('api/token/', obtain_auth_token),  # DRF token authentication
] + org_urls + sadmin_urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)