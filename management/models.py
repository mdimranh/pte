from django.db import models

from accounts.models import User


class Plan(models.Model):
    title = models.TextField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_accounts = models.PositiveIntegerField()
    thumbnail = models.ImageField(upload_to="plan/thumbnail")

class PlanPurchase(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(User, on_delete=models.CASCADE)
