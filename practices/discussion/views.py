from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from accounts.security.permission import (IsStudentPermission,
                                          IsStudentPermissionOrReadonly, IsSuperAdmin)

from ..blank.models import Blank, RWBlank, ReadingBlank
from ..describe_image.models import DescribeImage
from ..dictation.models import Dictation
from ..highlight_incorrect_word.models import HighlightIncorrectWord
from ..highlight_summary.models import HighlightSummary
from ..missing_word.models import MissingWord
from ..multi_choice.models import MultiChoice, MultiChoiceReading
from ..read_aloud.models import ReadAloud
from ..reorder_paragraph.models import ReorderParagraph
from ..repeat_sentence.models import RepeatSentence
from ..retell_sentence.models import RetellSentence
from ..short_question.models import ShortQuestion
from ..summarize.models import Summarize, SummarizeSpoken
from ..write_easy.models import WriteEasy
from .models import Discussion
from .serializers import (DiscussionListSerializer, DiscussionSerializer,
                          DynamicSerializer)

ds = DynamicSerializer(Discussion)

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        page_number = self.request.query_params.get(self.page_query_param, 1)
        page_size = self.get_page_size(self.request)

        total = self.page.paginator.count
        start_index = (page_number - 1) * page_size + 1
        end_index = start_index + len(data) - 1
        next_page_number = self.page.next_page_number() if self.page.has_next() else None
        previous_page_number = self.page.previous_page_number() if self.page.has_previous() else None

        links = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        }

        return Response({
            'total': total,
            'start_index': start_index,
            'end_index': end_index,
            'links': links,
            'next': bool(next_page_number),
            'prev': bool(previous_page_number),
            "results": data
        })

class ReadAloudDiscussionListView(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        read_aloud_id = self.kwargs.get('id')
        return Discussion.objects.filter(parent__isnull=True, read_aloud__id=read_aloud_id)

class HighlightSummaryDiscussionListView(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        highlight_summary_id = self.kwargs.get('id')
        return Discussion.objects.filter(parent__isnull=True, highlight_summary__id=highlight_summary_id)

class SummarizeDiscussionListView(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        summarize_id = self.kwargs.get('id')
        return Discussion.objects.filter(parent__isnull=True, summarize__id=summarize_id)

class MultiChoiceDiscussionListView(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        multi_choice_id = self.kwargs.get('id')
        return Discussion.objects.filter(parent__isnull=True, multi_choice__id=multi_choice_id)

class MissingWordDiscussionListView(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        missing_word_id = self.kwargs.get('id')
        return Discussion.objects.filter(parent__isnull=True, missing_word__id=missing_word_id)

class DictationDiscussionListView(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        dictation_id = self.kwargs.get('id')
        return Discussion.objects.filter(parent__isnull=True, dictation__id=dictation_id)

class BlankDiscussionListView(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        blank_id = self.kwargs.get('id')
        return Discussion.objects.filter(parent__isnull=True, blank__id=blank_id)

class RWBlankDiscussionListView(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        rwblank_id = self.kwargs.get('id')
        return Discussion.objects.filter(parent__isnull=True, read_write_blank__id=rwblank_id)

query = {
    "read_aloud": lambda id: Discussion.objects.filter(parent__isnull=True, read_aloud__id=id).order_by('id'),
    "highlight_summary": lambda id: Discussion.objects.filter(parent__isnull=True, highlight_summary__id=id).order_by('id'),
    "summarize": lambda id: Discussion.objects.filter(parent__isnull=True, summarize__id=id).order_by('id'),
    "summarize_spoken": lambda id: Discussion.objects.filter(parent__isnull=True, summarize_spoken__id=id).order_by('id'),
    "multi_choice": lambda id: Discussion.objects.filter(parent__isnull=True, multi_choice__id=id).order_by('id'),
    "multi_choice_reading": lambda id: Discussion.objects.filter(parent__isnull=True, multi_choice_reading__id=id).order_by('id'),
    "missing_word": lambda id: Discussion.objects.filter(parent__isnull=True, missing_word__id=id).order_by('id'),
    "dictation": lambda id: Discussion.objects.filter(parent__isnull=True, dictation__id=id).order_by('id'),
    "blank_listening": lambda id: Discussion.objects.filter(parent__isnull=True, blank__id=id).order_by('id'),
    "blank_reading": lambda id: Discussion.objects.filter(parent__isnull=True, blank_reading__id=id).order_by('id'),
    "read_write_blank": lambda id: Discussion.objects.filter(parent__isnull=True, read_write_blank__id=id).order_by('id'),
    "describe_image": lambda id: Discussion.objects.filter(parent__isnull=True, describe_image__id=id).order_by('id'),
    "highlight_incorrect_word": lambda id: Discussion.objects.filter(parent__isnull=True,  highlight_incorrect_word__id=id).order_by('id'),
    "reorder_paragraph": lambda id: Discussion.objects.filter(parent__isnull=True, reorder_paragraph__id=id).order_by('id'),
    "repeat_sentence": lambda id: Discussion.objects.filter(parent__isnull=True, repeat_sentence__id=id).order_by('id'),
    "retell_sentence": lambda id: Discussion.objects.filter(parent__isnull=True, retell_sentence__id=id).order_by('id'),
    "short_question": lambda id: Discussion.objects.filter(parent__isnull=True, short_question__id=id).order_by('id'),
    "write_easy": lambda id: Discussion.objects.filter(parent__isnull=True, write_easy__id=id).order_by('id')
}

class DiscussionListView(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        id = self.kwargs.get('id')
        model = self.kwargs.get('model')

        queryset = query.get(model)
        
        if queryset:
            return queryset(id)
        else:
            raise Http404

class DiscussionCreateView(CreateAPIView):
    permission_classes = [IsStudentPermission]
    serializer_class = DiscussionSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
    "blank_reading": ReadingBlank,
    "read_write_blank": RWBlank,
    "describe_image": DescribeImage,
    "highlight_incorrect_word": HighlightIncorrectWord,
    "reorder_paragraph": ReorderParagraph,
    "repeat_sentence": RepeatSentence,
    "retell_sentence": RetellSentence,
    "short_question": ShortQuestion,
    "write_easy": WriteEasy
}

from rest_framework.parsers import MultiPartParser
class DiscussionAdd(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsStudentPermission]
    def post(self, request, *args, **kwargs):
        model = self.kwargs.get('model')
        fields = ['body', 'images', 'parent']
        _for = _models.get(model)
        if _for is None:
            raise Http404
        serializer = ds.generate(fields, _for, model)(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LikeDiscussion(APIView):
    permission_classes = [IsStudentPermission | IsSuperAdmin | IsAdminUser]
    def get(self, request, id):
        discussion = Discussion.objects.filter(id=id).first()
        if discussion is None:
            return Response({
                "error": "Discussion not found."
            }, status = status.HTTP_404_NOT_FOUND)
        if request.user in discussion.like.all():
            discussion.like.remove(request.user)
            discussion.save()
            return Response({
                "message": "Successfully removed from liked."
            })
        else:
            discussion.like.add(request.user)
            discussion.save()
            return Response({
                "message": "Successfully liked."
            })

class DiscussionDelete(APIView):
    permission_classes = [IsStudentPermission]
    def delete(self, request, id):
        discussion = Discussion.objects.filter(id=id).first()
        if discussion is None:
            return Response({
                "error": "Discussion not found."
            }, status = status.HTTP_404_NOT_FOUND)
        if discussion.user != request.user:
            return Response({
                "error": "You dont have permission to delete this."
            }, status = status.HTTP_401_UNAUTHORIZED)
        discussion.delete()
        return Response({
            "message": "Discussion deleted successfully."
        })