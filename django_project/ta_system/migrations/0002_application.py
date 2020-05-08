# Generated by Django 3.0.2 on 2020-04-24 03:13

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ta_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_preferences', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), size=None)),
                ('instructor_preferences', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), size=None)),
                ('major', models.CharField(max_length=50)),
                ('grad_year', models.IntegerField()),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_system.Semester')),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
            },
        ),
    ]
