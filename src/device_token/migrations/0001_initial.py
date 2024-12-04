from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeviceToken",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("device_token", models.CharField(max_length=40)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="device_tokens",
                        to="user.user",
                    ),
                ),
            ],
        ),
    ]
