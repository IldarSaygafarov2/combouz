from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name="Категория", max_length=155)
    slug = models.SlugField(verbose_name="Слаг", default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    SIZE_CHOICES = [
        (f'{i}', f'{i} мм')
        for i in range(1, 30)
    ]

    QUANTITY_CHOICES = [
        (i, i)
        for i in range(1, 30)
    ]
    CORNICE_TYPE_CHOICES = [
        ('Алюминевый', 'Алюминевый'),
        ('Пластиковый', 'Пластиковый')
    ]

    CONTROL_TYPE_CHOICES = [
        ('', 'Ручной'),
        ('С электроприводом', 'С электроприводом'),
    ]

    name = models.CharField(verbose_name="Название товара", unique=True, max_length=155)
    width = models.CharField(verbose_name="Ширина", max_length=15, choices=SIZE_CHOICES)
    height = models.CharField(verbose_name="Высота", max_length=15, choices=SIZE_CHOICES)
    is_left_control = models.BooleanField(verbose_name="Управление слева?", default=False, blank=True)
    is_right_control = models.BooleanField(verbose_name="Управление Справа?", default=False, blank=True)
    quantity = models.IntegerField(verbose_name="Количество", choices=QUANTITY_CHOICES)
    cornice_type = models.CharField(blank=True, choices=CORNICE_TYPE_CHOICES, max_length=50)
    control_type = models.CharField(blank=True, choices=CONTROL_TYPE_CHOICES, max_length=50)
    manufacturer_country = models.CharField(verbose_name="Страна производитель", max_length=150)
    fabric_type = models.CharField(verbose_name="Тип ткани", max_length=150)
    property = models.CharField(verbose_name="Свойство", max_length=100)
    dimming = models.SmallIntegerField(verbose_name="Затемнение", default=0)
    price = models.CharField(verbose_name="Цена", max_length=100)
    description = models.TextField(verbose_name="Описание продукта")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_options")
    option_main = models.CharField(verbose_name="Главная характеристика", max_length=200)
    option_additional = models.TextField(verbose_name="Описание характеристики")

    def __str__(self):
        return f"{self.product}: {self.option_main}"


class ProductImage(models.Model):
    def make_folder_path(self, filename):
        return f"photos/products/{filename}"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    photo = models.ImageField(verbose_name="Фото", upload_to=make_folder_path)
