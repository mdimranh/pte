
from django.shortcuts import redirect
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import User
from .serializers import (RegistrationSerializer, UserCreateSerializer,
                          UserDetailsSerializer, UserProfileUpdateSerializer)


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

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        serializer = UserProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(id=request.user.id).update(**serializer.data)
            get_user = User.objects.get(id=request.user.id)
            serializer = UserDetailsSerializer(get_user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserProfileUpload(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        picture = request.FILES.get('picture')
        if picture:
            user = request.user
            user.picture = picture
            user.save()
            return Response({
                'picture': user.picture.url
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'No picture provided'
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)