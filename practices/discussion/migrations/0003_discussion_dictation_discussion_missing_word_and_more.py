# Generated by Django 4.2.4 on 2023-10-12 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictation', '0001_initial'),
        ('missing_word', '0001_initial'),
        ('summarize', '0002_summarize_appeared_summarize_bookmark_and_more'),
        ('multi_choice', '0002_multichoice_single'),
        ('discussion', '0002_discussion_highlight_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='dictation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dictation.dictation'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='missing_word',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='missing_word.missingword'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='multi_choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='multi_choice.multichoice'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='summarize',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='summarize.summarize'),
        ),
    ]