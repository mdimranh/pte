from django.db import models
from accounts.models import User

class Payment(models.Model):
    author = models.ForeignKey(User, related_name='payment', on_delete=models.SET_NULL, blank=True, null=True)
    tran_id = models.CharField(max_length=255, blank=True, null=True)
    val_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    store_amount = models.FloatField(blank=True, null=True)
    card_type = models.CharField(max_length=100, blank=True, null=True)
    card_no = models.CharField(max_length=255, blank=True, null=True)
    bank_tran_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    tran_date = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(blank=True, null=True)