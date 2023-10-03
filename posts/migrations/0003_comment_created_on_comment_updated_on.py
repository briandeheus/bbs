# Generated by Django 4.2.5 on 2023-10-03 06:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_alter_post_options_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2023, 10, 3, 6, 24, 57, 795148, tzinfo=datetime.timezone.utc
                ),
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="comment",
            name="updated_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
