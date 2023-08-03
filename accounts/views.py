
from django.shortcuts import redirect
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (RegistrationSerializer, UserCreateSerializer,
                          UserDetailsSerializer)


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserCreateSerializer(user, context=self.get_serializer_context()).data)

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserDetailsSerializer(self.request.user)
        return Response(serializer.data)

