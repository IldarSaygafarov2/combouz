from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static
from django.urls import reverse

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=15)
    email = models.EmailField(unique=True, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_name_by_email(self):
        return str(self.email).split("@")[0]

    class Meta:
        verbose_name = "Пользовать"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]


class Category(models.Model):
    name = models.CharField(verbose_name="Категория", max_length=155)
    slug = models.SlugField(verbose_name="Слаг", default="")

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def get_category_products_count(self):
        products = self.categories.all()
        return products.count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    SIZE_CHOICES = [
        (f'{i} мм', f'{i} мм')
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
        ('Ручной', 'Ручной'),
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
    price = models.SmallIntegerField(verbose_name="Цена", default=0)
    description = models.TextField(verbose_name="Описание продукта")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories", default=None)
    slug = models.SlugField(default="")
    created_at = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True, null=True)
    color = models.CharField(verbose_name="Цвет", max_length=100, default="")
    discount = models.IntegerField(verbose_name="Размер скидки", blank=True, null=True)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"product_slug": self.slug})

    def get_first_photo(self):
        images = self.images.all()
        if not images:
            return static("images/soon.png")
        return images[0].photo.url

    def get_choices_range(self):
        return [choice[0] for choice in self.SIZE_CHOICES]

    def get_quantity_range(self):
        return [choice[0] for choice in self.QUANTITY_CHOICES]

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


class ProjectsGallery(models.Model):
    title = models.CharField(verbose_name="Заголовок проекта", max_length=255)
    subtitle = models.CharField(verbose_name="Подзаголовок проекта", max_length=255)
    photo = models.ImageField(verbose_name="Фото проекта", upload_to="gallery/projects/", default="")

    def __str__(self):
        return f"{self.title}: {self.subtitle}"

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Галерея проектов"


class Client(models.Model):
    name = models.CharField(verbose_name="Название клиента", max_length=255)
    photo = models.ImageField(verbose_name="Логотип клиента", upload_to="clients/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(verbose_name="Текст комментария")

    def __str__(self):
        return f"{self.author}: {self.product}"


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(verbose_name="Имя", max_length=150)
    last_name = models.CharField(verbose_name="Фамилия", max_length=150)
    email = models.EmailField(verbose_name="Почта")
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=15)
    mounting_type = models.CharField(verbose_name="Тип монтажа", max_length=255)
    address = models.CharField(verbose_name="Адрес", max_length=255)
    comment = models.CharField(verbose_name="Комментарий", max_length=1000, default="")
    delivery_type = models.CharField(verbose_name="Тип доставки", max_length=150)
    delivery_option = models.CharField(verbose_name="Вариант доставки", max_length=150, default="")

    def __str__(self):
        return self.first_name


class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        return sum([item.get_total_price for item in order_products])

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        return sum([item.quantity for item in order_products])


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="order_products")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return int(self.product.price) * self.quantity


class Feedback(models.Model):
    body = models.TextField(verbose_name="Текст отзыва")
    feedback_author = models.CharField(verbose_name="Имя автора отзыва", max_length=255)
    author_company = models.CharField(verbose_name="Компания автора отзыва", max_length=255)
    avatar = models.ImageField(verbose_name="Фото автора отзыва", upload_to="feedback/author/")

    def __str__(self):
        return f"{self.feedback_author}: {self.body[:100]}..."

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class FAQ(models.Model):
    youtube_video_url = models.URLField(verbose_name="Ссылка на видео",
                                        help_text="Нужно поставить ссылку из встраивания видео с ютуба")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class MessageTelegram(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=True, blank=True)
    product_msg = models.TextField(blank=True, null=True)
    basket_msg = models.TextField(blank=True, null=True)


