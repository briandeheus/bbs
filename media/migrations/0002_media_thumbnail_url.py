# Generated by Django 4.2.5 on 2023-10-22 08:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("media", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="media",
            name="thumbnail_url",
            field=models.CharField(default="", max_length=1000),
            preserve_default=False,
        ),
    ]
