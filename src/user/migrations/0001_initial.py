# Generated by Django 4.0 on 2024-11-10 18:03

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("item", "0002_alter_item_id"),
        ("eatery", "0005_alter_eatery_campus_area"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("netid", models.CharField(blank=True, max_length=10, null=True)),
                ("given_name", models.CharField(blank=True, max_length=30, null=True)),
                ("family_name", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "google_id",
                    models.CharField(blank=True, max_length=50, null=True, unique=True),
                ),
                ("email", models.EmailField(blank=True, max_length=255, null=True)),
                (
                    "favorite_items",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "favorite_eateries",
                    models.ManyToManyField(
                        blank=True, related_name="favorited_by", to="eatery.Eatery"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserFCMDevice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("netid", models.CharField(blank=True, max_length=10, null=True)),
                ("name", models.CharField(default="User", max_length=40)),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "favorite_eateries",
                    models.ManyToManyField(
                        blank=True, related_name="favorited_by", to="eatery.Eatery"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserFCMDevice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "fcm_device",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fcm_django.fcmdevice",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fcm_device",
                        to="user.user",
                    ),
                ),
            ],
        ),
    ]
