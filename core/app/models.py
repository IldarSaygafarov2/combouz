from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name="Категория", max_length=155)
    slug = models.SlugField(verbose_name="Слаг", default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
