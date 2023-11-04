# Generated by Django 4.2.4 on 2023-11-04 05:32

from django.db import migrations
import utils.fields
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('multi_choice', '0002_multichoice_single'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multichoice',
            name='options',
        ),
        migrations.AddField(
            model_name='multichoice',
            name='_options',
            field=utils.fields.jsonField(blank=True, null=True, validators=[utils.validators.JsonValidator]),
        ),
    ]