from django.db import models

from accounts.models import User


class Dictation(models.Model):
    title = models.TextField(unique=True)
    audio = models.FileField(upload_to="media/dictation/%Y/%m/%d/")
    content = models.TextField()
    bookmark = models.ManyToManyField(User, blank=True, related_name='dictation_bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    class Meta:
        ordering = ["-id"]
