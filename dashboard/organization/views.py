from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.security.permission import IsOrganizationPermission
from accounts.serializers import UserCreateSerializer, UserDetailsSerializer
from management.models import Group, Purchase
from practices.discussion.views import CustomPagination

from .serializers import *


class RegistrationView(GenericAPIView):
    serializer_class = CreateStudentSerializer
    permission_classes = (IsOrganizationPermission,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserCreateSerializer(user, context=self.get_serializer_context()).data)

class StudenListView(ListAPIView):
    serializer_class = StudentListSerializer
    permission_classes = [IsOrganizationPermission]
    pagination_class = CustomPagination
    def get_queryset(self):
        queryset = User.objects.filter(profile__organization__id=self.request.user.id)
        return queryset

class StudenDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    queryset = User.objects.all()
    serializer_class = StudentDetailsSerializer
    permission_classes = [IsOrganizationPermission]

class AssignPlanView(APIView):
    permission_classes=[IsOrganizationPermission]
    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        serializer = AssignPlanSerializer(data=data)
        if serializer.is_valid():
            purchase = Purchase.objects.get(id=serializer.validated_data['plan'].id)
            purchase.student.add(serializer.validated_data['student'])
            return Response({
                "message": "Plan assigned successfully."
            })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ChangePassword(APIView):
    permission_classes=[IsOrganizationPermission]
    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        serializer = ChangePasswordSerializer(data=data)
        if serializer.is_valid():
            if request.user.check_password(serializer.validated_data['my_password']):
                student = User.objects.get(id=serializer.validated_data['student'].id)
                student.set_password(serializer.validated_data['new_password'])
                return Response({
                    "message": "Password changed successfully."
                })
            return Response({
                "my_password": ["Incorrect password."]
            })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class GroupListView(ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsOrganizationPermission]
    def get_queryset(self):
        queryset = Group.objects.filter(organization__id=self.request.user.id)
        return queryset
    

class GroupCreateView(GenericAPIView):
    permission_classes = [IsOrganizationPermission]
    serializer_class = GroupCreateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data['organization'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        return Response(GroupCreateSerializer(group, context=self.get_serializer_context()).data)
    