from django.db import models

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
    title = models.TextField()
    read_aloud = models.ManyToManyField(ReadAloud, related_name="speaking_mocktest")
    repeat_sentence = models.ManyToManyField(RepeatSentence, related_name="speaking_mocktest")
    retell_sentence = models.ManyToManyField(RetellSentence, related_name="speaking_mocktest")
    describe_image = models.ManyToManyField(DescribeImage, related_name="speaking_mocktest")
    short_question = models.ManyToManyField(ShortQuestion, related_name="speaking_mocktest")

class WrittingMocktest(models.Model):
    title = models.TextField()
    summarize = models.ManyToManyField(Summarize,  related_name="writting_mocktest")
    write_essay = models.ManyToManyField(WriteEasy,  related_name="writting_mocktest")

class ReadingMocktest(models.Model):
    title = models.TextField()
    summarize_spoken = models.ManyToManyField(SummarizeSpoken, related_name="reading_mocktest")
    multi_choice_reading_multi_answer = models.ManyToManyField(MultiChoiceReading, related_name="reading_mocktest_multi")
    multi_choice_reading_single_answer = models.ManyToManyField(MultiChoiceReading, related_name="reading_mocktest_single")
    highlight_summary = models.ManyToManyField(HighlightSummary, related_name="reading_mocktest")
    reading_balnk = models.ManyToManyField(ReadingBlank, related_name="reading_mocktest")
    missing_word = models.ManyToManyField(MissingWord, related_name="reading_mocktest")
    highlight_incorrect_word = models.ManyToManyField(HighlightIncorrectWord, related_name="reading_mocktest")
    dictation = models.ManyToManyField(Dictation, related_name="reading_mocktest")

class ListeningMocktest(models.Model):
    title = models.TextField()
    reading_writting_blank = models.ManyToManyField(RWBlank,  related_name="listening_mocktest")
    multi_choice_multi_answer = models.ManyToManyField(MultiChoice,  related_name="listening_mocktest_multi")
    multi_choice_single_answer = models.ManyToManyField(MultiChoice, related_name="listening_mocktest_single")
    reorder_paragraph = models.ManyToManyField(ReorderParagraph,  related_name="listening_mocktest")
    blank = models.ManyToManyField(Blank, related_name="listening_mocktest")

class FullMocktest(models.Model):
    title = models.TextField()
    read_aloud = models.ManyToManyField(ReadAloud, related_name="full_mocktest")
    repeat_sentence = models.ManyToManyField(RepeatSentence, related_name="full_mocktest")
    retell_sentence = models.ManyToManyField(RetellSentence, related_name="full_mocktest")
    describe_image = models.ManyToManyField(DescribeImage, related_name="full_mocktest")
    short_question = models.ManyToManyField(ShortQuestion, related_name="full_mocktest")
    summarize = models.ManyToManyField(Summarize,  related_name="full_mocktest")
    write_essay = models.ManyToManyField(WriteEasy,  related_name="full_mocktest")
    summarize_spoken = models.ManyToManyField(SummarizeSpoken, related_name="full_mocktest")
    multi_choice_reading_multi_answer = models.ManyToManyField(MultiChoiceReading, related_name="full_mocktest_multi_reading")
    multi_choice_reading_single_answer = models.ManyToManyField(MultiChoiceReading, related_name="full_mocktest_single_reading")
    highlight_summary = models.ManyToManyField(HighlightSummary, related_name="full_mocktest")
    reading_balnk = models.ManyToManyField(ReadingBlank, related_name="full_mocktest")
    missing_word = models.ManyToManyField(MissingWord, related_name="full_mocktest")
    highlight_incorrect_word = models.ManyToManyField(HighlightIncorrectWord, related_name="full_mocktest")
    dictation = models.ManyToManyField(Dictation, related_name="full_mocktest")
    reading_writting_blank = models.ManyToManyField(RWBlank,  related_name="full_mocktest")
    multi_choice_multi_answer = models.ManyToManyField(MultiChoice,  related_name="full_mocktest_multi")
    multi_choice_single_answer = models.ManyToManyField(MultiChoice, related_name="full_mocktest_single")
    reorder_paragraph = models.ManyToManyField(ReorderParagraph,  related_name="full_mocktest")
    blank = models.ManyToManyField(Blank, related_name="full_mocktest")