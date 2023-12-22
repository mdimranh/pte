# Generated by Django 4.2.7 on 2023-12-04 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('highlight_incorrect_word', '0003_alter_highlightincorrectword_options'),
        ('short_question', '0002_alter_shortquestion_options'),
        ('multi_choice', '0007_alter_multichoice_options_and_more'),
        ('highlight_summary', '0008_alter_highlightsummary_options'),
        ('missing_word', '0004_alter_missingword_options'),
        ('reorder_paragraph', '0002_alter_reorderparagraph_options'),
        ('retell_sentence', '0002_alter_retellsentence_options'),
        ('blank', '0005_alter_blank_options_alter_readingblank_options_and_more'),
        ('describe_image', '0002_alter_describeimage_options'),
        ('repeat_sentence', '0004_alter_repeatsentence_options'),
        ('summarize', '0004_alter_summarizespoken_options'),
        ('dictation', '0002_alter_dictation_options'),
        ('read_aloud', '0004_alter_readaloud_options'),
        ('write_easy', '0003_alter_writeeasy_options'),
        ('mocktest', '0005_alter_fullmocktest_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fullmocktest',
            name='blank',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='blank.blank'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='describe_image',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='describe_image.describeimage'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='dictation',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='dictation.dictation'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='highlight_incorrect_word',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='highlight_incorrect_word.highlightincorrectword'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='highlight_summary',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='highlight_summary.highlightsummary'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='missing_word',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='missing_word.missingword'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='multi_choice_multi_answer',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest_multi', to='multi_choice.multichoice'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='multi_choice_reading_multi_answer',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest_multi_reading', to='multi_choice.multichoicereading'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='multi_choice_reading_single_answer',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest_single_reading', to='multi_choice.multichoicereading'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='multi_choice_single_answer',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest_single', to='multi_choice.multichoice'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='read_aloud',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='read_aloud.readaloud'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='reading_balnk',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='blank.readingblank'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='reading_writting_blank',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='blank.rwblank'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='reorder_paragraph',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='reorder_paragraph.reorderparagraph'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='repeat_sentence',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='repeat_sentence.repeatsentence'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='retell_sentence',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='retell_sentence.retellsentence'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='short_question',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='short_question.shortquestion'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='summarize',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='summarize.summarize'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='summarize_spoken',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='summarize.summarizespoken'),
        ),
        migrations.AlterField(
            model_name='fullmocktest',
            name='write_essay',
            field=models.ManyToManyField(blank=True, related_name='full_mocktest', to='write_easy.writeeasy'),
        ),
        migrations.AlterField(
            model_name='listeningmocktest',
            name='blank',
            field=models.ManyToManyField(blank=True, related_name='listening_mocktest', to='blank.blank'),
        ),
        migrations.AlterField(
            model_name='listeningmocktest',
            name='multi_choice_multi_answer',
            field=models.ManyToManyField(blank=True, related_name='listening_mocktest_multi', to='multi_choice.multichoice'),
        ),
        migrations.AlterField(
            model_name='listeningmocktest',
            name='multi_choice_single_answer',
            field=models.ManyToManyField(blank=True, related_name='listening_mocktest_single', to='multi_choice.multichoice'),
        ),
        migrations.AlterField(
            model_name='listeningmocktest',
            name='reading_writting_blank',
            field=models.ManyToManyField(blank=True, related_name='listening_mocktest', to='blank.rwblank'),
        ),
        migrations.AlterField(
            model_name='listeningmocktest',
            name='reorder_paragraph',
            field=models.ManyToManyField(blank=True, related_name='listening_mocktest', to='reorder_paragraph.reorderparagraph'),
        ),
        migrations.AlterField(
            model_name='readingmocktest',
            name='dictation',
            field=models.ManyToManyField(blank=True, related_name='reading_mocktest', to='dictation.dictation'),
        ),
        migrations.AlterField(
            model_name='readingmocktest',
            name='highlight_incorrect_word',
            field=models.ManyToManyField(blank=True, related_name='reading_mocktest', to='highlight_incorrect_word.highlightincorrectword'),
        ),
        migrations.AlterField(
            model_name='readingmocktest',
            name='highlight_summary',
            field=models.ManyToManyField(blank=True, related_name='reading_mocktest', to='highlight_summary.highlightsummary'),
        ),
        migrations.AlterField(
            model_name='readingmocktest',
            name='missing_word',
            field=models.ManyToManyField(blank=True, related_name='reading_mocktest', to='missing_word.missingword'),
        ),
        migrations.AlterField(
            model_name='readingmocktest',
            name='multi_choice_reading_multi_answer',
            field=models.ManyToManyField(blank=True, related_name='reading_mocktest_multi', to='multi_choice.multichoicereading'),
        ),
        migrations.AlterField(
            model_name='readingmocktest',
            name='multi_choice_reading_single_answer',
            field=models.ManyToManyField(blank=True, related_name='reading_mocktest_single', to='multi_choice.multichoicereading'),
        ),
        migrations.AlterField(
            model_name='readingmocktest',
            name='reading_balnk',
            field=models.ManyToManyField(blank=True, related_name='reading_mocktest', to='blank.readingblank'),
        ),
        migrations.AlterField(
            model_name='readingmocktest',
            name='summarize_spoken',
            field=models.ManyToManyField(blank=True, related_name='reading_mocktest', to='summarize.summarizespoken'),
        ),
        migrations.AlterField(
            model_name='speakingmocktest',
            name='describe_image',
            field=models.ManyToManyField(blank=True, related_name='speaking_mocktest', to='describe_image.describeimage'),
        ),
        migrations.AlterField(
            model_name='speakingmocktest',
            name='read_aloud',
            field=models.ManyToManyField(blank=True, related_name='speaking_mocktest', to='read_aloud.readaloud'),
        ),
        migrations.AlterField(
            model_name='speakingmocktest',
            name='repeat_sentence',
            field=models.ManyToManyField(blank=True, related_name='speaking_mocktest', to='repeat_sentence.repeatsentence'),
        ),
        migrations.AlterField(
            model_name='speakingmocktest',
            name='retell_sentence',
            field=models.ManyToManyField(blank=True, related_name='speaking_mocktest', to='retell_sentence.retellsentence'),
        ),
        migrations.AlterField(
            model_name='speakingmocktest',
            name='short_question',
            field=models.ManyToManyField(blank=True, related_name='speaking_mocktest', to='short_question.shortquestion'),
        ),
        migrations.AlterField(
            model_name='writtingmocktest',
            name='summarize',
            field=models.ManyToManyField(blank=True, related_name='writting_mocktest', to='summarize.summarize'),
        ),
        migrations.AlterField(
            model_name='writtingmocktest',
            name='write_essay',
            field=models.ManyToManyField(blank=True, related_name='writting_mocktest', to='write_easy.writeeasy'),
        ),
    ]