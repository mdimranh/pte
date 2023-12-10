from django.db import models

from accounts.models import User


class ExamCountdown(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_date = models.DateTimeField()

    class Meta:
        ordering = ["-id"]

class TargetScore(models.Model):
    # Define choices as tuples of (value, human-readable name)
    THIRTY_FIVE = 35
    FIFTY_FIVE = 55
    SEVENTY_FIVE = 75
    NINETY = 90

    YOUR_CHOICES = [
        (THIRTY_FIVE, '35'),
        (FIFTY_FIVE, '55'),
        (SEVENTY_FIVE, '75'),
        (NINETY, '90'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=YOUR_CHOICES)

    class Meta:
        ordering = ["-id"]