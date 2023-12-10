from django.db import models

from accounts.models import User


class DescribeImage(models.Model):
    title = models.TextField(unique=True)
    image = models.FileField(upload_to="media/describe_image/%Y/%m/%d/")
    reference_text = models.TextField()
    bookmark = models.ManyToManyField(User, blank=True, related_name='di_bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    class Meta:
        ordering = ["-id"]
