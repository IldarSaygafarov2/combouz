# Generated by Django 4.2.2 on 2023-09-10 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_messagetelegram"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="username",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
