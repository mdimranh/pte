from django.contrib.postgres.fields import ArrayField
from django.db import models

from accounts.models import User
from utils.fields import jsonField
from utils.validators import JsonValidator

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

class Blank(models.Model):
    title = models.TextField()
    audio = models.FileField(upload_to="media/blank/%Y/%m/%d/")
    sentence = ArrayField(models.TextField())
    answers = jsonField(schema=schema, validators=[JsonValidator])
    bookmark = models.ManyToManyField(User, blank=True, related_name='blank_bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)


rwb_schema = {
    "type" : "list",
    "properties" : {
        "index": {
            "type": "string"
        },
        "options": {
            "type": "list",
            "properties": {
                "type": "string"
            }
        },
        "answer": {
            "type": "string"
        },
        "type": "object"
    },
}

class RWBlank(models.Model):
    title = models.TextField()
    sentence = ArrayField(models.TextField())
    options = jsonField(schema=rwb_schema, validators=[JsonValidator])
    bookmark = models.ManyToManyField(User, blank=True, related_name='rwblank_bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    @property
    def option_list(self):
        options = self.options
        for option in options:
            del option['answer']
        return options

