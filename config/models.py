from django.db import models
from django.contrib.postgres.fields import ArrayField

class Enum(models.Model):
    name = models.CharField(max_length=255)
    uid = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    options = ArrayField(models.CharField(max_length=255), blank=True, null=True)

