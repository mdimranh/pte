from django.contrib.postgres.fields import ArrayField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from accounts.models import User

from ..describe_image.models import DescribeImage
from ..dictation.models import Dictation
from ..highlight_summary.models import HighlightSummary
from ..missing_word.models import MissingWord
from ..multi_choice.models import MultiChoice
from ..read_aloud.models import ReadAloud
from ..reorder_paragraph.models import ReorderParagraph
from ..repeat_sentence.models import RepeatSentence
from ..retell_sentence.models import RetellSentence
from ..short_question.models import ShortQuestion
from ..summarize.models import Summarize
from ..write_easy.models import WriteEasy


class Answer(models.Model):
    read_aloud = models.ForeignKey(ReadAloud, blank=True, null=True, on_delete=models.CASCADE)
    summarize = models.ForeignKey(Summarize, blank=True, null=True, on_delete=models.CASCADE)
    highlight_summary = models.ForeignKey(HighlightSummary, blank=True, null=True, on_delete=models.CASCADE)
    multi_choice = models.ForeignKey(MultiChoice, blank=True, null=True, on_delete=models.CASCADE)
    missing_word = models.ForeignKey(MissingWord, blank=True, null=True, on_delete=models.CASCADE)
    dictation = models.ForeignKey(Dictation, blank=True, null=True, on_delete=models.CASCADE)
    write_easy = models.ForeignKey(WriteEasy, blank=True, null=True, on_delete=models.CASCADE)
    repeat_sentence = models.ForeignKey(RepeatSentence, blank=True, null=True, on_delete=models.CASCADE)
    retell_sentence = models.ForeignKey(RetellSentence, blank=True, null=True, on_delete=models.CASCADE)
    describe_image = models.ForeignKey(DescribeImage, blank=True, null=True, on_delete=models.CASCADE)
    short_question = models.ForeignKey(ShortQuestion, blank=True, null=True, on_delete=models.CASCADE)
    reorder_paragraph = models.ForeignKey(ReorderParagraph, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio = models.FileField(blank=True, null=True, upload_to="media/answer/%Y/%m/%d/", validators=[FileExtensionValidator(['wav'])])
    summarize_text = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    answers = ArrayField(models.TextField(), blank=True, null=True)
    score = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    # return score for specific answer
    def scores(self):
        score = self.score
        if getattr(self, 'read_aloud', None) is not None:
            return score
        if getattr(self, 'summarize', None) is not None:
            return score
        if getattr(self, 'highlight_summary', None) is not None:
            return score
        else: return {}

    def max_score(self):
        if getattr(self, 'multi_choice', None) is not None:
            return len(self.multi_choice.right_options)
        elif getattr(self, 'missing_word', None) is not None:
            return len(self.missing_word.right_options)
        elif getattr(self, 'dictation', None) is not None:
            return len(self.dictation.content.split(" "))
        elif getattr(self, 'highlight_summary', None) is not None:
            return 1
        return 0

    # def answer_details(self):
    #     if getattr(self, 'dictation', None) is not None:
    #         get_dictation = Dictation.objects.get(**getattr(self, 'dictation'))
    #         return get_score(get_dictation.content, self.answer)

@receiver(post_delete, sender=Answer)
def delete_file(sender, instance, **kwargs):
    if instance.audio:
        instance.audio.delete(False)