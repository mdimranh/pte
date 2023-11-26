from django.db import models
from django.utils import timezone

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
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['title', 'category']

COUPON_TYPE = (
    ('fixed', 'Fixed'),
    ('percentage', 'Percentage'),
)

class Coupon(models.Model):
    title = models.TextField()
    code = models.CharField(max_length=15)
    type = models.CharField(max_length=20, choices=COUPON_TYPE)
    amount = models.IntegerField()
    max_use = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class PromoBanner(models.Model):
    title = models.TextField()
    link = models.URLField()
    show_after = models.IntegerField()
    image = models.ImageField(upload_to="promo_banner")
    active = models.BooleanField(default=True)