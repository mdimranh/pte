from django.contrib.postgres.fields import ArrayField
from django.db import models


class ReadAloud(models.Model):
    title = models.TextField()
    article = models.TextField()
    tested = models.IntegerField(default=0)

    def __str__(self):
        return self.title if len(self.title) < 25 else self.title[:25]+"..."
