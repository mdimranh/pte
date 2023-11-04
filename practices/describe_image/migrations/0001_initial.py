# Generated by Django 4.2.4 on 2023-11-04 09:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DescribeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(unique=True)),
                ('image', models.FileField(upload_to='media/describe_image/%Y/%m/%d/')),
                ('reference_text', models.TextField()),
                ('prediction', models.BooleanField(default=False)),
                ('appeared', models.IntegerField(default=0)),
                ('bookmark', models.ManyToManyField(blank=True, related_name='di_bookmark', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]