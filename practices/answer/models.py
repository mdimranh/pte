from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from accounts.models import User

from ..read_aloud.models import ReadAloud
from ..summarize.models import Summarize


class Answer(models.Model):
    read_aloud = models.ForeignKey(ReadAloud, blank=True, null=True, on_delete=models.CASCADE)
    summarize = models.ForeignKey(Summarize, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio = models.FileField(blank=True, null=True, upload_to="answer/%Y/%m/%d/", validators=[FileExtensionValidator(['mp3', 'wav'])])
    summarize_text = models.TextField(blank=True, null=True)
    score = models.JSONField(default=dict)

    # return score for specific answer
    def scores(self):
        score = self.score
        if getattr(self, 'read_aloud', None) is not None:
            return {
                'score': score['score'],
                'content_score': score['content_score'],
                'user_speech': score['user_speech'],
                'reference_text': score['reference_text'],
                'word_highlight': score['word_highlight'],
                'fluency_score': score['fluency_score'],
                'total_score': score['total_score']
            }
        if getattr(self, 'summarize', None) is not None:
            return {
                'Content': round(score['Content'] * 100, 2),
                'Form': score['Form'],
                'Grammar': score['Grammar'],
                'Vocabulary': score['Vocabulary'],
                'Overall': round(score['Overall'] * 100, 2)
            }
        else: return {}

@receiver(post_delete, sender=Answer)
def delete_file(sender, instance, **kwargs):
    if instance.audio:
        instance.audio.delete(False)