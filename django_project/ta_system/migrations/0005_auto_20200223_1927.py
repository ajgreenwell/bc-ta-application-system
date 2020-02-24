# Generated by Django 3.0.2 on 2020-02-24 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ta_system', '0004_auto_20200220_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_num',
            field=models.CharField(max_length=14, unique=True, verbose_name='Course Number (e.g. CSCI110101)'),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ta_system.Instructor'),
        ),
    ]
