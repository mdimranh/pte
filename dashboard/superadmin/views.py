from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView, UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.security.permission import IsSuperAdmin
from practices.dictation.models import Dictation
from practices.highlight_summary.models import HighlightSummary
from practices.missing_word.models import MissingWord
from practices.multi_choice.models import MultiChoice
from practices.read_aloud.models import ReadAloud
from practices.repeat_sentence.models import RepeatSentence
from practices.retell_sentence.models import RetellSentence
from practices.summarize.models import Summarize
from practices.write_easy.models import WriteEasy

from .models import StudyMaterial
from .serializers import (AdminUserSerializer, CreateOrganizationSerializer,
                          OrganizationSerializer, StudyMaterialSerializer,
                          SuperAdminCreateSerializer)


class AdminUserAddView(GenericAPIView):
    serializer_class = SuperAdminCreateSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(AdminUserSerializer(user, context=self.get_serializer_context()).data)

class AdminUserListView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = AdminUserSerializer
    
    def get_queryset(self):
        queryset = User.objects.filter(Q(is_admin=True) | Q(is_staff=True)).exclude(id=self.request.user.id)
        return queryset

class DeleteAdminUserView(DestroyAPIView):
    lookup_field = 'id'
    serializer_class = AdminUserSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        queryset = User.objects.filter(id=self.kwargs['id']).exclude(id=self.request.user.id)
        return queryset
    

class TestStatisticsView(APIView):
    # permission_classes = [IsAdminUser]
    def get(self, request):
        datas = {
            "read_aloud": ReadAloud.objects.all().count(),
            "missing_word": MissingWord.objects.all().count(),
            "summarize_written": Summarize.objects.all().count(),
            "dictation": Dictation.objects.all().count(),
            "highlight_summary": HighlightSummary.objects.all().count(),
            "multi_choice_multiple_answer": MultiChoice.objects.filter(single=False).count(),
            "multi_choice_single_answer": MultiChoice.objects.filter(single=True).count(),
            "write_easy": WriteEasy.objects.all().count(),
            "repeat_sentence": RepeatSentence.objects.all().count(),
            "retell_sentence": RetellSentence.objects.all().count()
        }
        return JsonResponse(datas)


class StudyMaterialCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer

class StudyMaterialListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyMaterialSerializer

    def get_queryset(self):
        category = self.kwargs.get('category')
        available_categories = ['all', 'prediction', 'template', 'study_material']
        if category not in available_categories:
            raise Http404("Page not found")
        if category == 'all':
            if self.request.user.is_student:
                profile = Profile.objects.filter(user=request.user)
                if profile is not None and profile.organization is not None:
                    return StudyMaterial.objects.all()
                else:
                    return StudyMaterial.objects.filter(premium=False)
        if self.request.user.is_student:
            profile = Profile.objects.filter(user=request.user)
            if profile is not None and profile.organization is not None:
                return StudyMaterial.objects.filter(category=category)
            else:
                return StudyMaterial.objects.filter(premium=False, category=category)
        return StudyMaterial.objects.filter(category=category)
    


class StudyMaterialDestroyAPIView(DestroyAPIView):
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer


class OrgRegistrationView(GenericAPIView):
    serializer_class = CreateOrganizationSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(OrganizationSerializer(user, context=self.get_serializer_context()).data)

class OrgPasswordChange(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, *args, **kwargs):
        data = request.data
        if "password" not in data:
            return Response({
                "password": "Pasword can't be null."
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        id = self.kwargs.get('id')
        user = User.objects.filter(id=id, is_organization=True).first()
        if user is None:
            return Response({
                "error": "Organization not found."
            }, status=status.HTTP_404_NOT_FOUND)
        user.set_password(data['password'])
        user.save()
        return Response({
            "success": "Password have been changed successfully."
        })

class OrganizationListView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = OrganizationSerializer
    queryset = User.objects.filter(is_organization=True)

