# Generated by Django 4.2.7 on 2023-12-04 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0012_discussion_blank_reading'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discussion',
            options={'ordering': ['-id']},
        ),
    ]
