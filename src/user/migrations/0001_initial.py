# Generated by Django 4.0 on 2024-10-30 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eatery', '0005_alter_eatery_campus_area'),
        ('item', '0002_alter_item_id'),
        ('fcm_django', '0011_fcmdevice_fcm_django_registration_id_user_id_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('netid', models.CharField(blank=True, max_length=10, null=True)),
                ('name', models.CharField(default='User', max_length=40)),
                ('is_admin', models.BooleanField(default=False)),
                ('favorite_eateries', models.ManyToManyField(blank=True, related_name='favorited_by', to='eatery.Eatery')),
                ('favorite_items', models.ManyToManyField(blank=True, related_name='favorited_by', to='item.Item')),
            ],
        ),
        migrations.CreateModel(
            name='UserFCMDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fcm_device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fcm_django.fcmdevice')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fcm_device', to='user.user')),
            ],
        ),
    ]
