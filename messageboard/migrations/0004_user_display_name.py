# Generated by Django 4.2.5 on 2023-10-03 04:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("messageboard", "0003_user_profile_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="display_name",
            field=models.CharField(default="", max_length=1024),
            preserve_default=False,
        ),
    ]
