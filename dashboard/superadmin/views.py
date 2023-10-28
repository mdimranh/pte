from django.http import Http404, JsonResponse
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

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
from .serializers import StudyMaterialSerializer


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