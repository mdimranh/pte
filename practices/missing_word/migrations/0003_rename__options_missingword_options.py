# Generated by Django 4.2.4 on 2023-11-04 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('missing_word', '0002_remove_missingword_options_missingword__options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='missingword',
            old_name='_options',
            new_name='options',
        ),
    ]