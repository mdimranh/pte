# Generated by Django 4.2.4 on 2023-10-22 15:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0007_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='student',
            field=models.ManyToManyField(related_name='org_group', to=settings.AUTH_USER_MODEL),
        ),
    ]
