from django.db import models

from ..practices.describe_image.models import DescribeImage
from ..practices.read_aloud.models import ReadAloud
from ..practices.repeat_sentence.models import RepeatSentence
from ..practices.retell_sentence.models import RetellSentence
from ..practices.short_question.models import ShortQuestion


class SpeakingMocktest(models.Model):
    title = models.models.TextField()
    read_aloud = models.ForeignKey(ReadAloud, on_delete=models.CASCADE)
    repeat_sentence = models.ForeignKey(RepeatSentence, on_delete=models.CASCADE)
    retell_sentence = models.ForeignKey(RetellSentence, on_delete=models.CASCADE)
    describe_image = models.ForeignKey(DescribeImage, on_delete=models.CASCADE)
    short_question = models.ForeignKey(ShortQuestion, on_delete=models.CASCADE)
