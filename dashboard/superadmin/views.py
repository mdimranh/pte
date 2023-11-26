from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.security.permission import IsSuperAdmin
from practices.blank.models import Blank, RWBlank
from practices.describe_image.models import DescribeImage
from practices.dictation.models import Dictation
from practices.discussion.models import Discussion
from practices.highlight_incorrect_word.models import HighlightIncorrectWord
from practices.highlight_summary.models import HighlightSummary
from practices.missing_word.models import MissingWord
from practices.multi_choice.models import MultiChoice, MultiChoiceReading
from practices.read_aloud.models import ReadAloud
from practices.reorder_paragraph.models import ReorderParagraph
from practices.repeat_sentence.models import RepeatSentence
from practices.retell_sentence.models import RetellSentence
from practices.short_question.models import ShortQuestion
from practices.summarize.models import Summarize, SummarizeSpoken
from practices.write_easy.models import WriteEasy
from utils.pagination import CustomPagination

from .models import Coupon, StudyMaterial
from .serializers import *


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
    pagination_class = CustomPagination

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
            else:
                return StudyMaterial.objects.all()
        if self.request.user.is_student:
            profile = Profile.objects.filter(user=request.user)
            if profile is not None and profile.organization is not None:
                return StudyMaterial.objects.filter(category=category)
            else:
                return StudyMaterial.objects.filter(premium=False, category=category)
        return StudyMaterial.objects.filter(category=category)

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response([])
    


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

class OrganizationUpdateApiView(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, id):
        try:
            organization = User.objects.get(id=id, is_organization=True)
        except:
            return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrganizationUpdateSerializer(data=request.data, context={'id': id})
        if serializer.is_valid():
            update = serializer.save()
            return Response({
                "success": "Organization updated successfully."
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class CouponListCreateAPIView(ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class CouponRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    lookup_field = 'pk'


class DiscussionCountView(APIView):
    def get(self, request, *args, **kwargs):
        query = {
            "read_aloud": Discussion.objects.filter(read_aloud__id__isnull=False).count(),
            "highlight_summary": Discussion.objects.filter(highlight_summary__id__isnull=False).count(),
            "summarize_written": Discussion.objects.filter(summarize__id__isnull=False).count(),
            "summarize_spoken": Discussion.objects.filter(summarize_spoken__id__isnull=False).count(),
            "multi_choice_single_answer": Discussion.objects.filter(multi_choice__id__isnull=False, multi_choice__single=True).count(),
            "multi_choice_multi_answer": Discussion.objects.filter(multi_choice__id__isnull=False, multi_choice__single=False).count(),
            "multi_choice_reading_single_answer": Discussion.objects.filter(multi_choice_reading__id__isnull=False, multi_choice_reading__single=True).count(),
            "multi_choice_reading_multi_answer": Discussion.objects.filter(multi_choice_reading__id__isnull=False, multi_choice_reading__single=False).count(),
            "missing_word": Discussion.objects.filter(missing_word__id__isnull=False).count(),
            "dictation": Discussion.objects.filter(dictation__id__isnull=False).count(),
            "blank": Discussion.objects.filter(blank__id__isnull=False).count(),
            "read_write_blank": Discussion.objects.filter(read_write_blank__id__isnull=False).count(),
            "describe_image": Discussion.objects.filter(describe_image__id__isnull=False).count(),
            "highlight_incorrect_word": Discussion.objects.filter(highlight_incorrect_word__id__isnull=False).count(),
            "reorder_paragraph": Discussion.objects.filter(reorder_paragraph__id__isnull=False).count(),
            "repeat_sentence": Discussion.objects.filter(repeat_sentence__id__isnull=False).count(),
            "retell_sentence": Discussion.objects.filter(retell_sentence__id__isnull=False).count(),
            "short_question": Discussion.objects.filter(short_question__id__isnull=False).count(),
            "write_easy": Discussion.objects.filter(write_easy__id__isnull=False).count()
        }
        return JsonResponse(query)

_models = {
    "read_aloud": ReadAloud,
    "highlight_summary": HighlightSummary,
    "summarize": Summarize,
    "summarize_spoken": SummarizeSpoken,
    "multi_choice": MultiChoice,
    "multi_choice_reading": MultiChoiceReading,
    "missing_word": MissingWord,
    "dictation": Dictation,
    "blank": Blank,
    "read_write_blank": RWBlank,
    "describe_image": DescribeImage,
    "highlight_incorrect_word": HighlightIncorrectWord,
    "reorder_paragraph": ReorderParagraph,
    "repeat_sentence": RepeatSentence,
    "retell_sentence": RetellSentence,
    "short_question": ShortQuestion,
    "write_easy": WriteEasy
}

class ModelWiseDiscussion(APIView):
    # permission_classes = [IsSuperAdmin]
    def get(self, request, *args, **kwargs):
        model = self.kwargs.get('model')
        fields = ['id', 'title']
        _for = _models.get(model)
        if _for is None:
            raise Http404
        datas = _for.objects.all()
        serializer_class = DynamicSerializer(_for).generate(fields, _for, model)
        serializer = serializer_class(instance=datas, many=True)
        return Response(serializer.data)

class PromoBannerView(ListCreateAPIView):
    permission_classes = [IsAdminUser | IsSuperAdmin]
    serializer_class = PromoBannerSerializer
    queryset = PromoBanner.objects.all()

class PromoBannerRUDView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    permission_classes = [IsAdminUser | IsSuperAdmin]
    serializer_class = PromoBannerSerializer
    queryset = PromoBanner.objects.all()