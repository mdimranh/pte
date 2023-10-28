from django.db import models

STUDY_MATERIAL_CHOICES = (
    ("prediction", "Prediction"),
    ("template", "Template"),
    ("study_material", "Study Material")
)

class StudyMaterial(models.Model):
    title = models.TextField()
    category = models.CharField(max_length=20, choices=STUDY_MATERIAL_CHOICES)
    file = models.FileField(upload_to="study_material/%Y/%m/%d/")
    premium = models.BooleanField(default=False)

    class Meta:
        unique_together = ['title', 'category']
