# Generated by Django 4.2.7 on 2023-12-04 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_rename_picture_user_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialaccount',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-id'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
