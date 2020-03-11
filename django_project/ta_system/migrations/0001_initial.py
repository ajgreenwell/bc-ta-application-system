# Generated by Django 3.0.3 on 2020-03-11 00:06

from django.conf import settings
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
                ('name', models.CharField(max_length=60, validators=[ta_system.validators.DataValidator(message="Please enter the name of the course, e.g. 'Computer Science I'.", regex='\\S+( \\S+)*')])),
                ('days_of_week', models.CharField(max_length=13, validators=[ta_system.validators.DataValidator(message="Please specify the days of the week this class meets separated by slashes, e.g. 'M/W/F'.", regex='[MTWRFAS](/[MTWRFAS])*')], verbose_name='Days of the Week (e.g. M/W/F)')),
                ('start_time', models.TimeField(validators=[ta_system.validators.DataValidator(message="Please enter the time this class starts (in millitary time), e.g. '14:00'.", regex='\\d{2}:\\d{2}(:\\d{2})*')], verbose_name='Start Time (e.g. 14:00)')),
                ('end_time', models.TimeField(validators=[ta_system.validators.DataValidator(message="Please enter the time this class ends (in millitary time), e.g. '14:50'.", regex='\\d{2}:\\d{2}(:\\d{2})*')], verbose_name='End Time (e.g. 14:50)')),
                ('building', models.CharField(max_length=30, validators=[ta_system.validators.DataValidator(message="Please enter the building this class meets in, e.g. 'Fulton'.", regex='\\S+( \\S+)*')])),
                ('room_number', models.CharField(max_length=6, validators=[ta_system.validators.DataValidator(message="Please enter the number of the room this class meets in, e.g. '250'. One letter building codes may be included, e.g. '250S'.", regex='\\d+[A-Z]{0,1}')])),
                ('max_num_tas', models.PositiveIntegerField(default=2, validators=[ta_system.validators.DataValidator(message="Please enter the maximum number of TAs that can be assigned to this course, e.g. '3'. This field defaults to '2'.", regex='\\d+')], verbose_name='Max Number of TAs')),
            ],
        ),
        migrations.CreateModel(
            name='CourseID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=5, validators=[ta_system.validators.DataValidator(message="Please specify the year followed by the semester, e.g. '2020F'.", regex='\\d{4}[FS]')], verbose_name='Semester (e.g. 2020F)')),
                ('course_number', models.CharField(max_length=10, unique=True, validators=[ta_system.validators.DataValidator(message="Please enter a valid full course number, e.g. 'CSCI110101'.", regex='[A-Z]{4}\\d{6}')], verbose_name='Course Number (e.g. CSCI110101)')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, validators=[ta_system.validators.DataValidator(message="Please enter the name of the Instructor, e.g. 'Robert Muller'.", regex='\\S+( \\S+)*')])),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eagle_id', models.CharField(blank=True, max_length=8, null=True, unique=True, validators=[ta_system.validators.DataValidator(message="Please enter a valid 8-digit eagle id, e.g. '58704254'.", regex='\\d{8}')])),
                ('courses_taken', models.ManyToManyField(blank=True, related_name='students', to='ta_system.Course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='assigned_tas',
            field=models.ManyToManyField(blank=True, related_name='ta_courses', to='ta_system.Profile', verbose_name='Assigned TAs'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='ta_system.CourseID'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ta_system.Instructor'),
        ),
    ]
