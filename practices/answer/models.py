from django.core.validators import FileExtensionValidator
from django.db import models

from accounts.models import User

from ..read_aloud.models import ReadAloud


class Answer(models.Model):
    read_aloud = models.ForeignKey(ReadAloud, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio = models.FileField(blank=True, null=True, upload_to="uploads/%Y/%m/%d/", validators=[FileExtensionValidator(['mp3'])])
    content_score = models.IntegerField(default=0)
    pronunciation_score = models.IntegerField(default=0)
    fluency_score = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def scores(self):
        return {
            "content": self.content_score,
            "pronunciation": self.pronunciation_score,
            "fluency": self.fluency_score
        }