from django.contrib.postgres.fields import ArrayField
from django.db import models
from accounts.models import User
from django.apps import apps

class ReadAloud(models.Model):
    title = models.TextField()
    content = models.TextField()
    tested = models.IntegerField(default=0)
    bookmark = models.ManyToManyField(User, blank=True, related_name='bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    def practiced(self):
        return self.answer_set.count()

    def __str__(self):
        return self.title if len(self.title) < 25 else self.title[:25]+"..."

    class Meta:
        ordering = ["-id"]
