from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User
from utils.fields import jsonField
from utils.validators import JsonValidator


def validate_array_length(value, length=5):
    if len(value) != length:
        raise ValidationError(f"Array length must be {length}.")

schema = {
    "type" : "list",
    "properties" : {
        "index": {
            "type": "string"
        },
        "value": {
            "type": "string"
        },
        "type": "object"
    },
}

list_schema = {
    "type": "list",
    "properties": {
        "type": "string"
    }
}

class MultiChoice(models.Model):
    title = models.TextField(unique=True)
    audio = models.FileField(upload_to="media/multi_choice/%Y/%m/%d/")
    options = jsonField(schema=schema, validators=[JsonValidator])
    right_options = ArrayField(models.TextField())
    bookmark = models.ManyToManyField(User, blank=True, related_name='mc_bookmark')
    prediction = models.BooleanField(default=False)
    single = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    def practiced(self):
        return self.answer_set.count()

    def __str__(self):
        return self.title


class MultiChoiceReading(models.Model):
    title = models.TextField(unique=True)
    content = models.TextField()
    options = jsonField(schema=schema, validators=[JsonValidator])
    right_options = ArrayField(models.TextField())
    bookmark = models.ManyToManyField(User, blank=True, related_name='mcr_bookmark')
    prediction = models.BooleanField(default=False)
    single = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    def practiced(self):
        return self.answer_set.count()

    def __str__(self):
        return self.title