# Generated by Django 3.0.3 on 2020-04-04 07:22

import datetime
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import ta_system.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_number', models.CharField(help_text='A full BC course number, e.g. CSCI110101.', max_length=10, validators=[ta_system.validators.DataValidator(message="Please enter a valid full course number, e.g. 'CSCI110101'.", regex='[A-Z]{4}\\d{6}')], verbose_name='Course Number')),
                ('name', models.CharField(max_length=60, validators=[ta_system.validators.DataValidator(message="Please enter the name of the course, e.g. 'Computer Science I'.", regex='\\S+( \\S+)*')])),
                ('days_of_week', models.CharField(help_text='The 1-character days of the week this class meets, separated by slashes, eg. T/R.', max_length=13, validators=[ta_system.validators.DataValidator(message='M = Mon; T = Tues; W = Wed; R = Thurs; F = Fri; A = Sat; S = Sun... e.g. M/W/F', regex='[MTWRFAS](/[MTWRFAS])*')], verbose_name='Days of the Week')),
                ('start_time', models.TimeField(help_text='The time of day this class begins in millitary time, e.g. 14:00.', validators=[ta_system.validators.DataValidator(message="Please enter the time this class starts (in millitary time), e.g. '14:00'.", regex='\\d{2}:\\d{2}(:\\d{2})*')], verbose_name='Start Time')),
                ('end_time', models.TimeField(help_text='The time of day this class ends in millitary time, e.g. 14:50.', validators=[ta_system.validators.DataValidator(message="Please enter the time this class ends (in millitary time), e.g. '14:50'.", regex='\\d{2}:\\d{2}(:\\d{2})*')], verbose_name='End Time')),
                ('building', models.CharField(help_text='The building this class meets in, e.g. Fulton.', max_length=30, validators=[ta_system.validators.DataValidator(message="Please enter the building this class meets in, e.g. 'Fulton'.", regex='\\S+( \\S+)*')])),
                ('room_number', models.CharField(help_text='The room this class meets in. May contain a 1-digit building code, e.g. 250S.', max_length=6, validators=[ta_system.validators.DataValidator(message="Please enter the number of the room this class meets in, e.g. '250'. One letter building codes may be included, e.g. '250S'.", regex='\\d+[A-Z]{0,1}')], verbose_name='Room Number')),
                ('max_num_tas', models.PositiveIntegerField(default=2, help_text='The maximum number of teaching assistants that can be assigned to this course, e.g. 2.', validators=[ta_system.validators.DataValidator(message="Please enter the maximum number of TAs that can be assigned to this course, e.g. '3'. This field defaults to '2'.", regex='\\d+')], verbose_name='Max Number of TAs')),
            ],
            options={
                'ordering': ('semester', 'course_number'),
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of this instructor.', max_length=60, unique=True, validators=[ta_system.validators.DataValidator(message="Please enter the name of the Instructor, e.g. 'Robert Muller'.", regex='\\S+( \\S+)*')], verbose_name='Instructor')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(help_text='A year followed by a 1-digit semester code, e.g. 2020F.', max_length=5, unique=True, validators=[ta_system.validators.DataValidator(message="Please specify the year followed by the semester, e.g. '2020F'.", regex='\\d{4}[FS]')], verbose_name='Semester')),
            ],
            options={
                'ordering': ('-semester',),
            },
        ),
        migrations.CreateModel(
            name='SystemStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('date_changed', models.DateField(default=datetime.datetime(2020, 4, 4, 3, 22, 49, 106037))),
            ],
            options={
                'verbose_name': 'System Status',
                'verbose_name_plural': 'System Status',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eagle_id', models.CharField(blank=True, max_length=8, null=True, unique=True, validators=[ta_system.validators.DataValidator(message="Please enter a valid 8-digit eagle id, e.g. '58704254'.", regex='\\d{8}')], verbose_name='Eagle ID')),
                ('lab_hour_preferences', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('courses_taken', models.ManyToManyField(blank=True, related_name='students', to='ta_system.Course', verbose_name='Courses Taken')),
                ('ta_assignments', models.ManyToManyField(blank=True, to='ta_system.Course', verbose_name='TA Assignments')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'ordering': ('user__last_name',),
            },
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ta_system.Instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ta_system.Semester'),
        ),
        migrations.AddField(
            model_name='course',
            name='teaching_assistants',
            field=models.ManyToManyField(blank=True, to='ta_system.Profile', verbose_name='Teaching Assistants'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('semester', 'course_number')},
        ),
    ]
