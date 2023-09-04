# Generated by Django 4.2.3 on 2023-09-04 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_customer_user_alter_customer_comment_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
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
                ("body", models.CharField(max_length=500, verbose_name="Текст отзыва")),
                (
                    "feedback_author",
                    models.CharField(max_length=255, verbose_name="Имя автора отзыва"),
                ),
                (
                    "author_company",
                    models.CharField(
                        max_length=255, verbose_name="Компания автора отзыва"
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        upload_to="feedback/author/", verbose_name="Фото автора отзыва"
                    ),
                ),
            ],
        ),
    ]
