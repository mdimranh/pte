# Generated by Django 4.2.7 on 2023-11-26 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('write_easy', '0002_rename_content_writeeasy_question_and_more'),
        ('short_question', '0001_initial'),
        ('summarize', '0003_summarizespoken'),
        ('read_aloud', '0003_readaloud_appeared'),
        ('retell_sentence', '0001_initial'),
        ('describe_image', '0001_initial'),
        ('repeat_sentence', '0003_alter_repeatsentence_audio'),
        ('mocktest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speakingmocktest',
            name='describe_image',
        ),
        migrations.RemoveField(
            model_name='speakingmocktest',
            name='read_aloud',
        ),
        migrations.RemoveField(
            model_name='speakingmocktest',
            name='repeat_sentence',
        ),
        migrations.RemoveField(
            model_name='speakingmocktest',
            name='retell_sentence',
        ),
        migrations.RemoveField(
            model_name='speakingmocktest',
            name='short_question',
        ),
        migrations.RemoveField(
            model_name='writtingmocktest',
            name='summarize',
        ),
        migrations.RemoveField(
            model_name='writtingmocktest',
            name='write_essay',
        ),
        migrations.AddField(
            model_name='speakingmocktest',
            name='describe_image',
            field=models.ManyToManyField(to='describe_image.describeimage'),
        ),
        migrations.AddField(
            model_name='speakingmocktest',
            name='read_aloud',
            field=models.ManyToManyField(to='read_aloud.readaloud'),
        ),
        migrations.AddField(
            model_name='speakingmocktest',
            name='repeat_sentence',
            field=models.ManyToManyField(to='repeat_sentence.repeatsentence'),
        ),
        migrations.AddField(
            model_name='speakingmocktest',
            name='retell_sentence',
            field=models.ManyToManyField(to='retell_sentence.retellsentence'),
        ),
        migrations.AddField(
            model_name='speakingmocktest',
            name='short_question',
            field=models.ManyToManyField(to='short_question.shortquestion'),
        ),
        migrations.AddField(
            model_name='writtingmocktest',
            name='summarize',
            field=models.ManyToManyField(to='summarize.summarize'),
        ),
        migrations.AddField(
            model_name='writtingmocktest',
            name='write_essay',
            field=models.ManyToManyField(to='write_easy.writeeasy'),
        ),
    ]