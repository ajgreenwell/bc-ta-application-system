# Generated by Django 3.0.3 on 2020-03-11 01:10

from django.db import migrations, models
import django.db.models.deletion
import ta_system.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ta_system', '0004_auto_20200310_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=5, unique=True, validators=[ta_system.validators.DataValidator(message="Please specify the year followed by the semester, e.g. '2020F'.", regex='\\d{4}[FS]')], verbose_name='Semester (e.g. 2020F)')),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_id',
        ),
        migrations.AddField(
            model_name='course',
            name='course_number',
            field=models.CharField(default='CSCI110101', max_length=10, validators=[ta_system.validators.DataValidator(message="Please enter a valid full course number, e.g. 'CSCI110101'.", regex='[A-Z]{4}\\d{6}')], verbose_name='Course Number (e.g. CSCI110101)'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CourseID',
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ta_system.Semester'),
        ),
    ]