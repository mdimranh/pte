# Generated by Django 4.2.4 on 2023-11-22 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multi_choice', '0006_multichoicereading'),
        ('discussion', '0008_discussion_blank_discussion_describe_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='multi_choice_reading',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='multi_choice.multichoicereading'),
        ),
    ]