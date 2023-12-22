from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from accounts.models import User

from django.contrib.postgres.fields import ArrayField
from utils.fields import jsonField
from utils.validators import JsonValidator

from dashboard.superadmin.models import Coupon
from payment.models import Payment

class Plan(models.Model):
    title = models.TextField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_accounts = models.PositiveIntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="plan/thumbnail")

    class Meta:
        ordering = ["-id"]


validation_schema = {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string"
      },
      "saving": {
        "type": "integer"
      },
      "cost": {
        "type": "integer"
      },
      "quantity": {
        "type": "integer"
      }
    },
    "required": ["title", "saving", "cost", "quantity"]
  }
}

class OrganizationPackage(models.Model):
    title = models.TextField(unique=True)
    validity = models.IntegerField()
    premium_practice_access = models.BooleanField()
    mocktest_access = models.BooleanField()
    validation = jsonField(schema=validation_schema, validators=[JsonValidator(schema=validation_schema)])
    thumbnail = models.ImageField(upload_to="media/package/%Y/%m/%d/")

class StudentPackage(models.Model):
    title = models.TextField(unique=True)
    validity = models.IntegerField()
    premium_practice_access = models.BooleanField()
    mocktest_access = models.BooleanField()
    cost = models.IntegerField()
    pre_price = models.IntegerField()
    text = ArrayField(models.TextField(), blank=True, null=True)
    thumbnail = models.ImageField(upload_to="media/package/%Y/%m/%d/")

class Purchase(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, blank=True, null=True)
    org_package = models.ForeignKey(OrganizationPackage, on_delete=models.SET_NULL, blank=True, null=True)
    validation_id = models.IntegerField(blank=True, null=True)
    student_package = models.ForeignKey(StudentPackage, on_delete=models.SET_NULL, blank=True, null=True)
    organization = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organization")
    student = models.ManyToManyField(User, related_name="plan")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def available_account(self):
        return self.plan.maximum_accounts - self.student.count()

    class Meta:
        ordering = ["-id"]

GENDER = [
    ("male", "Male"),
    ("female", "Female"),
    ("others", "Other's")
]

class Group(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    userid = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER, blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    group = models.ForeignKey(Group, related_name='group', blank=True, null=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(User, on_delete=models.CASCADE, related_name="org", blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    org_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        ordering = ["-id"]

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, create = Profile.objects.get_or_create(
            user = instance
        )