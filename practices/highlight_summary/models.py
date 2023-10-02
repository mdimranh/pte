from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User


def validate_array_length(value, length=5):
    if len(value) != length:
        raise ValidationError(f"Array length must be {length}.")

class HighlightSummary(models.Model):
    title = models.TextField(unique=True)
    audio = models.FileField(upload_to="media/highlight_summary/%Y/%m/%d/")
    options = ArrayField(models.TextField(), size=5, validators=[validate_array_length])
    right_option = models.TextField()
    bookmark = models.ManyToManyField(User, blank=True, related_name='hs_bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    def practiced(self):
        return self.answer_set.count()

    def __str__(self):
        return self.title