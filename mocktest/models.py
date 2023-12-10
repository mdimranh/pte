from django.db import models
from django.utils import timezone

from practices.blank.models import Blank, RWBlank, ReadingBlank
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


class SpeakingMocktest(models.Model):
    title = models.TextField(unique=True)
    read_aloud = models.ManyToManyField(ReadAloud, related_name="speaking_mocktest", blank=True)
    repeat_sentence = models.ManyToManyField(RepeatSentence, related_name="speaking_mocktest", blank=True)
    retell_sentence = models.ManyToManyField(RetellSentence, related_name="speaking_mocktest", blank=True)
    describe_image = models.ManyToManyField(DescribeImage, related_name="speaking_mocktest", blank=True)
    short_question = models.ManyToManyField(ShortQuestion, related_name="speaking_mocktest", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

class WrittingMocktest(models.Model):
    title = models.TextField(unique=True)
    summarize = models.ManyToManyField(Summarize,  related_name="writting_mocktest", blank=True)
    write_essay = models.ManyToManyField(WriteEasy,  related_name="writting_mocktest", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

class ReadingMocktest(models.Model):
    title = models.TextField(unique=True)
    summarize_spoken = models.ManyToManyField(SummarizeSpoken, related_name="reading_mocktest", blank=True)
    multi_choice_reading_multi_answer = models.ManyToManyField(MultiChoiceReading, related_name="reading_mocktest_multi", blank=True)
    multi_choice_reading_single_answer = models.ManyToManyField(MultiChoiceReading, related_name="reading_mocktest_single", blank=True)
    highlight_summary = models.ManyToManyField(HighlightSummary, related_name="reading_mocktest", blank=True)
    reading_balnk = models.ManyToManyField(ReadingBlank, related_name="reading_mocktest", blank=True)
    missing_word = models.ManyToManyField(MissingWord, related_name="reading_mocktest", blank=True)
    highlight_incorrect_word = models.ManyToManyField(HighlightIncorrectWord, related_name="reading_mocktest", blank=True)
    dictation = models.ManyToManyField(Dictation, related_name="reading_mocktest", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

class ListeningMocktest(models.Model):
    title = models.TextField(unique=True)
    reading_writting_blank = models.ManyToManyField(RWBlank,  related_name="listening_mocktest", blank=True)
    multi_choice_multi_answer = models.ManyToManyField(MultiChoice,  related_name="listening_mocktest_multi", blank=True)
    multi_choice_single_answer = models.ManyToManyField(MultiChoice, related_name="listening_mocktest_single", blank=True)
    reorder_paragraph = models.ManyToManyField(ReorderParagraph,  related_name="listening_mocktest", blank=True)
    blank = models.ManyToManyField(Blank, related_name="listening_mocktest", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

class FullMocktest(models.Model):
    title = models.TextField(unique=True)
    read_aloud = models.ManyToManyField(ReadAloud, related_name="full_mocktest", blank=True)
    repeat_sentence = models.ManyToManyField(RepeatSentence, related_name="full_mocktest", blank=True)
    retell_sentence = models.ManyToManyField(RetellSentence, related_name="full_mocktest", blank=True)
    describe_image = models.ManyToManyField(DescribeImage, related_name="full_mocktest", blank=True)
    short_question = models.ManyToManyField(ShortQuestion, related_name="full_mocktest", blank=True)
    summarize = models.ManyToManyField(Summarize,  related_name="full_mocktest", blank=True)
    write_essay = models.ManyToManyField(WriteEasy,  related_name="full_mocktest", blank=True)
    summarize_spoken = models.ManyToManyField(SummarizeSpoken, related_name="full_mocktest", blank=True)
    multi_choice_reading_multi_answer = models.ManyToManyField(MultiChoiceReading, related_name="full_mocktest_multi_reading", blank=True)
    multi_choice_reading_single_answer = models.ManyToManyField(MultiChoiceReading, related_name="full_mocktest_single_reading", blank=True)
    highlight_summary = models.ManyToManyField(HighlightSummary, related_name="full_mocktest", blank=True)
    reading_balnk = models.ManyToManyField(ReadingBlank, related_name="full_mocktest", blank=True)
    missing_word = models.ManyToManyField(MissingWord, related_name="full_mocktest", blank=True)
    highlight_incorrect_word = models.ManyToManyField(HighlightIncorrectWord, related_name="full_mocktest", blank=True)
    dictation = models.ManyToManyField(Dictation, related_name="full_mocktest", blank=True)
    reading_writting_blank = models.ManyToManyField(RWBlank,  related_name="full_mocktest", blank=True)
    multi_choice_multi_answer = models.ManyToManyField(MultiChoice,  related_name="full_mocktest_multi", blank=True)
    multi_choice_single_answer = models.ManyToManyField(MultiChoice, related_name="full_mocktest_single", blank=True)
    reorder_paragraph = models.ManyToManyField(ReorderParagraph,  related_name="full_mocktest", blank=True)
    blank = models.ManyToManyField(Blank, related_name="full_mocktest", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]