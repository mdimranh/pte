# Generated by Django 4.2.7 on 2023-12-10 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('management', '0004_alter_group_options_alter_plan_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.payment'),
        ),
    ]
