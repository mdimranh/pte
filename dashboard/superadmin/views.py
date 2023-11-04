from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView)
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
        # try:
        #     user = serializer.save()
        # except IntegrityError:
        #     return Response({
        #         "email": "User already exists with this email.",
        #     }, status=status.HTTP_409_CONFLICT)
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
            return StudyMaterial.objects.all()
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

class OrganizationListView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = OrganizationSerializer
    queryset = User.objects.filter(is_organization=True)
