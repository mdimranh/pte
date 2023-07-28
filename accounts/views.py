
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import RegistrationSerializer


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()