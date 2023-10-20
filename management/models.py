from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User


class Plan(models.Model):
    title = models.TextField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_accounts = models.PositiveIntegerField()
    thumbnail = models.ImageField(upload_to="plan/thumbnail")


GENDER = [
    ("male", "Male"),
    ("female", "Female"),
    ("others", "Other's")
]

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    userid = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER, blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    group = models.TextField(blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, blank=True, null=True)
    organization = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organization", blank=True, null=True)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, create = Profile.objects.get_or_create(
            user = instance
        )