from django.contrib.postgres.fields import ArrayField
from django.db import models

from accounts.models import User

# new
from ..blank.models import Blank, RWBlank
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

TYPES = [
    ("discuss", "Discuss"),
    ("new_question", "New Question"),
    ("new_error", "New Error")
]

class Discussion(models.Model):
    read_aloud = models.ForeignKey(ReadAloud, blank=True, null=True, on_delete=models.CASCADE)
    highlight_summary = models.ForeignKey(HighlightSummary, blank=True, null=True, on_delete=models.CASCADE)
    summarize = models.ForeignKey(Summarize, blank=True, null=True, on_delete=models.CASCADE)
    summarize_spoken = models.ForeignKey(SummarizeSpoken, blank=True, null=True, on_delete=models.CASCADE)
    multi_choice = models.ForeignKey(MultiChoice, blank=True, null=True, on_delete=models.CASCADE)
    multi_choice_reading = models.ForeignKey(MultiChoiceReading, blank=True, null=True, on_delete=models.CASCADE)
    missing_word = models.ForeignKey(MissingWord, blank=True, null=True, on_delete=models.CASCADE)
    dictation = models.ForeignKey(Dictation, blank=True, null=True, on_delete=models.CASCADE)
    blank = models.ForeignKey(Blank, blank=True, null=True, on_delete=models.CASCADE)
    read_write_blank = models.ForeignKey(RWBlank, blank=True, null=True, on_delete=models.CASCADE)
    describe_image = models.ForeignKey(DescribeImage, blank=True, null=True, on_delete=models.CASCADE)
    reorder_paragraph = models.ForeignKey(ReorderParagraph, blank=True, null=True, on_delete=models.CASCADE)
    repeat_sentence = models.ForeignKey(RepeatSentence, blank=True, null=True, on_delete=models.CASCADE)
    retell_sentence = models.ForeignKey(RetellSentence, blank=True, null=True, on_delete=models.CASCADE)
    short_question = models.ForeignKey(ShortQuestion, blank=True, null=True, on_delete=models.CASCADE)
    write_easy = models.ForeignKey(WriteEasy, blank=True, null=True, on_delete=models.CASCADE)
    highlight_incorrect_word = models.ForeignKey(HighlightIncorrectWord, blank=True, null=True, on_delete=models.CASCADE)
    # answer = models.ForeignKey(Answer, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="discussion")
    body = models.TextField()
    type = models.CharField(max_length=30, choices=TYPES, default='discuss')
    images = ArrayField(models.ImageField(upload_to="media/discussion"), blank=True, null=True)
    like = models.ManyToManyField(User, related_name="like", blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_like(self):
        return self.like.count()

    def total_replies(self):
        return Discussion.objects.filter(parent=self.id).count()

    def __str__(self):
        return self.body if len(self.body) < 25 else self.body[:24]+"..."

