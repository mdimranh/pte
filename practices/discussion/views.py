from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import Discussion
from ..read_aloud.models import ReadAloud
from ..highlight_summary.models import HighlightSummary
from ..summarize.models import Summarize
from ..multi_choice.models import MultiChoice
from ..missing_word.models import MissingWord
from ..dictation.models import Dictation
from .serializers import DiscussionListSerializer, DiscussionSerializer, DynamicSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
    lookup_field = 'read_aloud'
    serializer_class = DiscussionListSerializer
    queryset = Discussion.objects.filter(parent__isnull=True)
    pagination_class = CustomPagination

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class HighlightSummaryDiscussionListView(ListAPIView):
    lookup_field = 'highlight_summary'
    serializer_class = DiscussionListSerializer
    queryset = Discussion.objects.filter(parent__isnull=True)
    pagination_class = CustomPagination

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class SummarizeDiscussionListView(ListAPIView):
    lookup_field = 'summarize'
    serializer_class = DiscussionListSerializer
    queryset = Discussion.objects.filter(parent__isnull=True)
    pagination_class = CustomPagination

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class MultiChoiceDiscussionListView(ListAPIView):
    lookup_field = 'multi_choice'
    serializer_class = DiscussionListSerializer
    queryset = Discussion.objects.filter(parent__isnull=True)
    pagination_class = CustomPagination

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class MissingWordDiscussionListView(ListAPIView):
    lookup_field = 'missing_word'
    serializer_class = DiscussionListSerializer
    queryset = Discussion.objects.filter(parent__isnull=True)
    pagination_class = CustomPagination

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class DictationDiscussionListView(ListAPIView):
    lookup_field = 'dictation'
    serializer_class = DiscussionListSerializer
    queryset = Discussion.objects.filter(parent__isnull=True)
    pagination_class = CustomPagination

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class DiscussionCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        model = self.kwargs.get('model')
        fields = ['body', 'images']
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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