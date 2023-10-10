
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .views import RegistrationView, UserDetailsView, UserProfileUpdateView, UserProfileUpload, UserLoginView, Home

urlpatterns = [
    path('auth/token', UserLoginView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/user/join', RegistrationView.as_view(), name='user_join'),
    path('user/profile', UserDetailsView.as_view(), name='user_profile'),
    path('user/profile/update', UserProfileUpdateView.as_view()),
    path('user/picture/upload', UserProfileUpload.as_view()),
    path('', Home.as_view())
]