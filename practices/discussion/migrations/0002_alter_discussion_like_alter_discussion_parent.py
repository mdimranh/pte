# Generated by Django 4.2.3 on 2023-07-27 17:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='parent',
            field=models.ManyToManyField(blank=True, to='discussion.discussion'),
        ),
    ]
