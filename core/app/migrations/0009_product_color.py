# Generated by Django 4.2.2 on 2023-08-23 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_product_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="color",
            field=models.CharField(default="", max_length=100, verbose_name="Цвет"),
        ),
    ]
