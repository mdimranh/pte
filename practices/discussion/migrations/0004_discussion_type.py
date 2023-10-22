# Generated by Django 4.2.4 on 2023-10-15 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0003_discussion_dictation_discussion_missing_word_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='type',
            field=models.CharField(choices=[('discuss', 'Discuss'), ('new_question', 'New Question'), ('new_error', 'New Error')], default='discuss', max_length=30),
        ),
    ]