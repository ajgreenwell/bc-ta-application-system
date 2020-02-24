# Generated by Django 3.0.3 on 2020-02-18 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=6)),
                ('course_num', models.CharField(max_length=6)),
                ('section_num', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('days_of_week', models.CharField(max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('building', models.CharField(max_length=30)),
                ('room', models.CharField(max_length=5)),
                ('max_num_tas', models.PositiveIntegerField(default=2)),
                ('num_tas', models.PositiveIntegerField(default=0)),
                ('course_num', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ta_system.CourseNumber')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ta_system.Instructor')),
            ],
        ),
    ]
