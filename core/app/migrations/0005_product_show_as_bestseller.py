# Generated by Django 4.2.3 on 2023-09-13 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_category_show_on_homepage"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="show_as_bestseller",
            field=models.BooleanField(
                default=False,
                help_text="При выборе, добавит данный товар на главную в раздел самых продоваемых товаров",
                verbose_name="Сделать самым продоваемым",
            ),
        ),
    ]
