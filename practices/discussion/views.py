from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.security.permission import (IsStudentPermission,
                                          IsStudentPermissionOrReadonly)

from ..dictation.models import Dictation
from ..highlight_summary.models import HighlightSummary
from ..missing_word.models import MissingWord
from ..multi_choice.models import MultiChoice
from ..read_aloud.models import ReadAloud
from ..summarize.models import Summarize
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

class DiscussionCreateView(CreateAPIView):
    permission_classes = [IsStudentPermission]
    serializer_class = DiscussionSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

_models = {
    "read_aloud": ReadAloud,
    "highlight_summary": HighlightSummary,
    "summarize": Summarize,
    "multi_choice": MultiChoice,
    "missing_word": MissingWord,
    "dictation": MissingWord,
}

class DiscussionAdd(APIView):
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
    permission_classes = [IsStudentPermission]
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