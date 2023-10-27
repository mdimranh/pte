from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from practices.dictation.models import Dictation
from practices.highlight_summary.models import HighlightSummary
from practices.missing_word.models import MissingWord
from practices.multi_choice.models import MultiChoice
from practices.read_aloud.models import ReadAloud
from practices.summarize.models import Summarize


class TestStatisticsView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        datas = {
            "read_aloud": ReadAloud.objects.all().count(),
            "missing_word": MissingWord.objects.all().count(),
            "summarize_written": Summarize.objects.all().count(),
            "dictation": Dictation.objects.all().count(),
            "highlight_summary": HighlightSummary.objects.all().count(),
            "multi_choice_multiple_answer": MultiChoice.objects.filter(single=False).count(),
            "multi_choice_single_answer": MultiChoice.objects.filter(single=True).count(),
        }
        return JsonResponse(datas)