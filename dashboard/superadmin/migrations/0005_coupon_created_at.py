# Generated by Django 4.2.7 on 2023-11-11 15:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0004_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 11, 11, 15, 57, 20, 979324, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]