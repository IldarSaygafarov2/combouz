# Generated by Django 4.2.2 on 2023-08-22 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_alter_projectsgallery_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectsgallery",
            name="photo",
            field=models.ImageField(
                default="", upload_to="gallery/projects/", verbose_name="Фото проекта"
            ),
        ),
    ]