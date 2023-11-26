# Generated by Django 4.2.4 on 2023-10-13 15:58

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0003_discussion_dictation_discussion_missing_word_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to='media/discussion'), blank=True, null=True, size=None),
        ),
    ]
