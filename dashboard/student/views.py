from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.security.permission import IsStudentPermission, IsSuperAdmin, IsOrganizationPermission
from rest_framework.permissions import IsAdminUser

from .models import ExamCountdown, TargetScore
from .serializers import ExamCountdownSerializer, TargetScoreSerializer


class ExamCountdownView(APIView):
    permission_classes = [IsStudentPermission | IsOrganizationPermission | IsAdminUser | IsSuperAdmin]
    def get(self, request):
        get_countdown = ExamCountdown.objects.filter(student=request.user).first()
        if get_countdown:
            serializer = ExamCountdownSerializer(instance=get_countdown)
            return Response(serializer.data)
        else:
            return Response({})
    def post(self, request):
        data = request.data
        serializer = ExamCountdownSerializer(data=data)
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    def put(self, request):
        data = request.data
        serializer = ExamCountdownSerializer(data=data)
        if serializer.is_valid():
            get_examcountdown = ExamCountdown.objects.filter(student=request.user).first()
            if get_examcountdown is None:
                serializer.save(student=request.user)
            else:
                get_examcountdown.exam_date = serializer.validated_data['exam_date']
                get_examcountdown.save()
                return Response(serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class TargetScoreView(APIView):
    permission_classes = [IsStudentPermission | IsOrganizationPermission | IsAdminUser | IsSuperAdmin]
    def get(self, request):
        get_target_score = TargetScore.objects.filter(student=request.user).first()
        if get_target_score:
            serializer = TargetScoreSerializer(instance=get_target_score)
            return Response(serializer.data)
        else:
            return Response({})
    def post(self, request):
        data = request.data
        serializer = TargetScoreSerializer(data=data)
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    def put(self, request):
        data = request.data
        serializer = TargetScoreSerializer(data=data)
        if serializer.is_valid():
            get_target_score = TargetScore.objects.filter(student=request.user).first()
            if get_target_score is None:
                serializer.save(student=request.user)
            else:
                get_target_score.score = serializer.validated_data['score']
                get_target_score.save()
                return Response(serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
