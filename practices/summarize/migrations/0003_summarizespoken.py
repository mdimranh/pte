# Generated by Django 4.2.7 on 2023-11-12 15:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('summarize', '0002_summarize_appeared_summarize_bookmark_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SummarizeSpoken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('reference_text', models.TextField()),
                ('audio', models.FileField(upload_to='media/summarize/%Y/%m/%d/')),
                ('prediction', models.BooleanField(default=False)),
                ('appeared', models.IntegerField(default=0)),
                ('bookmark', models.ManyToManyField(blank=True, related_name='ss_bookmark', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
