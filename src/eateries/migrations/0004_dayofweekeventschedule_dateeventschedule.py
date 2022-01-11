# Generated by Django 4.0 on 2022-01-10 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eateries', '0003_closedeventschedule_eatery_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayOfWeekEventSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('eatery', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eateries.eaterystore')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DateEventSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canonical_date', models.DateField()),
                ('start_timestamp', models.IntegerField()),
                ('end_timestamp', models.IntegerField()),
                ('eatery', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eateries.eaterystore')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
