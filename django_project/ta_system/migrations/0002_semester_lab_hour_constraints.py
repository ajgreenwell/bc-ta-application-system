# Generated by Django 3.0.3 on 2020-04-17 02:23

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ta_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='lab_hour_constraints',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list),
        ),
    ]