# Generated by Django 4.2.7 on 2023-12-04 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mocktest', '0007_fullmocktest_created_at_listeningmocktest_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fullmocktest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='listeningmocktest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='readingmocktest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='speakingmocktest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='writtingmocktest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
