# Generated by Django 4.2.4 on 2023-10-27 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('retell_sentence', '0001_initial'),
        ('answer', '0013_answer_repeat_sentence'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='retell_sentence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='retell_sentence.retellsentence'),
        ),
    ]