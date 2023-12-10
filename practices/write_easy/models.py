from django.db import models

from accounts.models import User


class WriteEasy(models.Model):
    title = models.TextField(unique=True)
    question = models.TextField()
    reference_text = models.TextField(blank=True, null=True)
    bookmark = models.ManyToManyField(User, blank=True, related_name='we_bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    class Meta:
        ordering = ["-id"]
