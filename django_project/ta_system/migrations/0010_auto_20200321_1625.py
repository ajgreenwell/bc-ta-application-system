# Generated by Django 3.0.3 on 2020-03-21 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ta_system.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ta_system', '0009_auto_20200319_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='days_of_week',
            field=models.CharField(max_length=13, validators=[ta_system.validators.DataValidator(message="Please specify the days of the week this class meets separatedby slashes, e.g. 'T/R'.", regex='[MTWRFAS](/[MTWRFAS])*')], verbose_name='Days of the Week (e.g. M/W/F)'),
        ),
        migrations.AlterField(
            model_name='course',
            name='max_num_tas',
            field=models.PositiveIntegerField(default=2, validators=[ta_system.validators.DataValidator(message="Please enter the maximum number of TAs that can be assigned to thiscourse, e.g. '3'. This field defaults to '2'.", regex='\\d+')], verbose_name='Max Number of TAs'),
        ),
        migrations.AlterField(
            model_name='course',
            name='room_number',
            field=models.CharField(max_length=6, validators=[ta_system.validators.DataValidator(message="Please enter the number of the room this class meets in, e.g. '250'.One letter building codes may be included, e.g. '250S'.", regex='\\d+[A-Z]{0,1}')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
