# Generated by Django 4.2.5 on 2023-10-04 02:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("messageboard", "0004_user_display_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="mastodon_registration_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
