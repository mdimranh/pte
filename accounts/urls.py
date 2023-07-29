
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .views import RegistrationView, UserDetailsView

urlpatterns = [
    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/user/join', RegistrationView.as_view(), name='user_join'),
    path('user/profile', UserDetailsView.as_view(), name='user_profile')
]