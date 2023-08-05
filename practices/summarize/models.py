from django.db import models

class Summarize(models.Model):
    title = models.TextField()
    content = models.TextField()
    tested = models.IntegerField(default=0)

    def __str__(self):
        return self.title

