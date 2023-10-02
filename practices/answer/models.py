from django.contrib.postgres.fields import ArrayField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from accounts.models import User

from ..highlight_summary.models import HighlightSummary
from ..missing_word.models import MissingWord
from ..multi_choice.models import MultiChoice
from ..read_aloud.models import ReadAloud
from ..summarize.models import Summarize


class Answer(models.Model):
    read_aloud = models.ForeignKey(ReadAloud, blank=True, null=True, on_delete=models.CASCADE)
    summarize = models.ForeignKey(Summarize, blank=True, null=True, on_delete=models.CASCADE)
    highlight_summary = models.ForeignKey(HighlightSummary, blank=True, null=True, on_delete=models.CASCADE)
    multi_choice = models.ForeignKey(MultiChoice, blank=True, null=True, on_delete=models.CASCADE)
    missing_word = models.ForeignKey(MissingWord, blank=True, null=True, on_delete=models.CASCADE)
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

@receiver(post_delete, sender=Answer)
def delete_file(sender, instance, **kwargs):
    if instance.audio:
        instance.audio.delete(False)