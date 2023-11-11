from django.db import models

from practices.describe_image.models import DescribeImage
from practices.read_aloud.models import ReadAloud
from practices.repeat_sentence.models import RepeatSentence
from practices.retell_sentence.models import RetellSentence
from practices.short_question.models import ShortQuestion

from practices.summarize.models import Summarize
from practices.write_easy.models import WriteEasy


class SpeakingMocktest(models.Model):
    title = models.TextField()
    read_aloud = models.ForeignKey(ReadAloud, on_delete=models.CASCADE)
    repeat_sentence = models.ForeignKey(RepeatSentence, on_delete=models.CASCADE)
    retell_sentence = models.ForeignKey(RetellSentence, on_delete=models.CASCADE)
    describe_image = models.ForeignKey(DescribeImage, on_delete=models.CASCADE)
    short_question = models.ForeignKey(ShortQuestion, on_delete=models.CASCADE)

class WrittingMockTest(models.Model):
    title = models.TextField()
    summarize = models.ForeignKey(Summarize, on_delete=models.CASCADE)
    write_essay = models.ForeignKey(WriteEasy, on_delete=models.CASCADE)
    