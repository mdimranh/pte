from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Options(models.Model):
    index = models.CharField(max_length=1)
    value = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def clean(self):
        # Check for uniqueness manually
        duplicates = Option.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id,
            index=self.index
        ).exclude(pk=self.pk)  # Exclude the current instance if it exists
        if duplicates.exists():
            raise ValidationError('Index must be unique.')
