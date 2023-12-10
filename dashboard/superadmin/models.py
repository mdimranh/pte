from django.db import models
from django.utils import timezone

STUDY_MATERIAL_CHOICES = (
    ("prediction", "Prediction"),
    ("template", "Template"),
    ("study_material", "Study Material")
)

class Topic(models.Model):
    title = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class StudyMaterial(models.Model):
    title = models.TextField(unique=True)
    category = models.CharField(max_length=20, choices=STUDY_MATERIAL_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.FileField(upload_to="study_material/%Y/%m/%d/")
    premium = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['title', 'category']
        ordering = ["-id"]

COUPON_TYPE = (
    ('fixed', 'Fixed'),
    ('percentage', 'Percentage'),
)

class Coupon(models.Model):
    title = models.TextField(unique=True)
    code = models.CharField(max_length=15)
    type = models.CharField(max_length=20, choices=COUPON_TYPE)
    amount = models.IntegerField()
    max_use = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

class PromoBanner(models.Model):
    title = models.TextField(default="unknown")
    link = models.URLField(blank=True, null=True)
    show_after = models.IntegerField(default=30)
    image = models.ImageField(upload_to="promo_banner", blank=True, null=True)
    active = models.BooleanField(default=False)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj