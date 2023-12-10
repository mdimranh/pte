from django.db import models

from accounts.models import User


class Summarize(models.Model):
    title = models.TextField()
    content = models.TextField()
    tested = models.IntegerField(default=0)
    bookmark = models.ManyToManyField(User, blank=True, related_name='summarize_bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def practiced(self):
        return self.answer_set.count()

class SummarizeSpoken(models.Model):
    title = models.TextField()
    reference_text = models.TextField()
    audio = models.FileField(upload_to="media/summarize/%Y/%m/%d/")
    bookmark = models.ManyToManyField(User, blank=True, related_name='ss_bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    class Meta:
        ordering = ["-id"]

