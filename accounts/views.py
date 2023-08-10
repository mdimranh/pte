
from django.shortcuts import redirect
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (RegistrationSerializer, UserCreateSerializer,
                          UserDetailsSerializer, UserProfileUpdateSerializer, UserLoginSerializer)


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer
    authentication_classes = ([])
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserCreateSerializer(user, context=self.get_serializer_context()).data)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            get_user = User.objects.filter(email=serializer.validated_data['email']).first()
            if get_user is None:
                return Response(
                    {
                        "error": "User not found with this email."
                    },
                    status = status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            if not get_user.check_password(serializer.validated_data['password']):
                return Response({"error":"Password is incorrect."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            refresh = RefreshToken.for_user(get_user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            )
        else:
            return Response({
                "error": serializer.error
            }, HTTP_422_UNPROCESSABLE_ENTITY)


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