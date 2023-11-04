from datetime import datetime, timedelta

from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView,
                                     RetrieveDestroyAPIView)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.security.permission import (IsOrganizationPermission,
                                          IsStudentPermission)
from accounts.serializers import UserCreateSerializer, UserDetailsSerializer
from management.models import Group, Purchase
from practices.discussion.views import CustomPagination

from ..student.models import ExamCountdown
from ..student.serializers import ExamCountdownListSerializer
from .serializers import *


class RegistrationView(GenericAPIView):
    serializer_class = CreateStudentSerializer
    permission_classes = [IsOrganizationPermission | IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserCreateSerializer(user, context=self.get_serializer_context()).data)

class StudenListView(ListAPIView):
    serializer_class = StudentListSerializer
    permission_classes = [IsOrganizationPermission | IsAdminUser]
    pagination_class = CustomPagination
    def get_queryset(self):
        if self.request.user.is_organization:
            queryset = User.objects.filter(profile__organization__id=self.request.user.id)
        else:
            queryset = User.objects.all()
        return queryset

class StudenRetriveDestroyApiView(RetrieveDestroyAPIView):
    lookup_field = "pk"
    queryset = User.objects.filter(is_student=True)
    serializer_class = StudentDetailsSerializer
    permission_classes = [IsOrganizationPermission | IsAdminUser]

class StudentUpdateApiView(APIView):
    permission_classes = [IsOrganizationPermission | IsAdminUser]
    def put(self, request, id):
        try:
            student = User.objects.get(id=id, is_student=True)
        except:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentUpdateSerializer(data=request.data, context={'id': id})
        if serializer.is_valid():
            update = serializer.save()
            return Response({
                "success": "Student updated successfully."
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentPasswordChange(APIView):
    permission_classes = [IsOrganizationPermission | IsAdminUser]
    def put(self, request, *args, **kwargs):
        data = request.data
        if "password" not in data:
            return Response({
                "password": "Pasword can't be null."
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        id = self.kwargs.get('id')
        user = User.objects.filter(id=id).first()
        if user is None:
            return Response({
                "error": "Student not found."
            }, status=status.HTTP_404_NOT_FOUND)
        user.set_password(data['password'])
        user.save()
        return Response({
            "success": "Password have been changed successfully."
        })

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

class ExamCalenderView(ListAPIView):
    permission_classes = [IsOrganizationPermission]
    serializer_class = ExamCountdownListSerializer
    queryset = ExamCountdown.objects.filter(exam_date__gte = timezone.now())

class StudentDataCounts(APIView):
    permission_classes = (IsStudentPermission,)
    def get(self, request):
        total_student = User.objects.filter(profile__organization = request.user).count()
        premium_student = Purchase.objects.filter(organization=request.user).aggregate(total_students=Count('student')).get('total_students')
        total_max_accounts = Purchase.objects.filter(organization=request.user).aggregate(total_max_accounts=Sum('plan__maximum_accounts')).get('total_max_accounts')
        total_student = 0 if total_student is None else total_student
        premium_student = 0 if premium_student is None else premium_student
        total_max_accounts = 0 if total_max_accounts is None else total_max_accounts
        print(total_student, premium_student)
        return Response({
            "total_student": total_student,
            "premium_student": premium_student,
            "free_students": total_student - premium_student,
            "account_remaining": max(0, total_max_accounts - total_student),
            "exam_in_7_days": 0,
            "score_75_90": 0,
            "score_55_45": 0,
            "score_55_0": 0
        })

class RecentJoinedStudentList(ListAPIView):
    permission_classes = [IsOrganizationPermission]
    serializer_class = StudentListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = User.objects.filter(profile__organization=self.request.user, date_joined__gte=timezone.now() - timedelta(days=30))
        return queryset
    
    