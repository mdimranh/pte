from django.db import models

from accounts.models import User


class RetellSentence(models.Model):
    title = models.TextField(unique=True)
    audio = models.FileField(upload_to="retell_sentence/%Y/%m/%d/")
    reference_text = models.TextField()
    bookmark = models.ManyToManyField(User, blank=True, related_name='retell_sentence_bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    class Meta:
        ordering = ["-id"]
