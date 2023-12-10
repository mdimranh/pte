from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
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

class ReorderParagraph(models.Model):
    title = models.TextField(unique=True)
    paragraph = models.TextField()
    options = jsonField(schema=schema, validators=[JsonValidator])
    answer_sequence = ArrayField(models.CharField(max_length=2))
    bookmark = models.ManyToManyField(User, blank=True, related_name='rp_bookmark')
    prediction = models.BooleanField(default=False)
    appeared = models.IntegerField(default=0)

    def practiced(self):
        return self.answer_set.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]