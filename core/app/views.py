import requests as req
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from core import settings

from .cart_utils import CartForAnonymousUser, CartForAuthenticatedUser, get_cart_data
from .forms import CommentForm, CustomUserAuthenticationForm, CustomUserCreationForm
from .models import (
    FAQ,
    Category,
    Client,
    Feedback,
    MessageTelegram,
    Product,
    ProjectsGallery,
)

DELIVERY_TYPES = {
    "takeaway": "Доставка курьером",
    "pickup": "Самовывоз - 0 сум",
    "install,size,delivery": "Установка, размер, доставка",
    "install,delivery": "Доставка и установка",
    "delivery-tashkent": "Доставка по городу Ташкент",
}

CORNICE_TYPES = {"aluminium": "Алюминевый", "plastic": "Пластиковый"}

CONTROL_TYPES = {"manual": "Ручной", "electro": "С электроприводом"}


def __make_product_variant_msg(product_data):
    if not product_data:
        return

    print(product_data.values())

    return f"""
Ширина: {product_data['item-width']}
Длина: {product_data['item-length']}
Управление: {'Слева' if product_data['item-control'] == 'left' else 'Справа'}
Кол-во: {product_data['item-count']}
Тип карниза: {CORNICE_TYPES[product_data['item-cornice-type']]}
Тип управления: {CONTROL_TYPES[product_data['item-control-type']]}
"""


def __make_basket_products_msg(basket_data):
    return f"""
Вариант Доставки: {DELIVERY_TYPES[basket_data['busket-delivery']]}
Фамилия: {basket_data['busket-surname']}
Имя: {basket_data['busket-name']}
Почта: {basket_data['busket-email']}
Номер телефона: {basket_data['busket-phone']}
Тип монтажа: {basket_data['busket-montage']}
Адрес: {basket_data['busket-address']}
Комментарий: {basket_data['busket-comment']}
Тип доставки: {DELIVERY_TYPES[basket_data['busket-delivery-type']]}
"""


def home_view(request):
    # querysets
    categories = Category.objects.filter(show_on_homepage=True)
    gallery_projects = ProjectsGallery.objects.all()
    feedbacks = Feedback.objects.all()
    videos = FAQ.objects.all()
    best_sellers_category = Category.objects.filter(show_as_bestseller=True).first()

    correct_videos = [
        video.youtube_video_url.replace("youtu.be", "www.youtube.com/embed")
        for video in videos
    ]

    context = {
        "registration_form": CustomUserCreationForm(),
        "login_form": CustomUserAuthenticationForm(),
        "gallery_projects": gallery_projects,
        "feedbacks": feedbacks,
        "videos_urls": correct_videos,
        "categories": categories,
        "best_sellers_category": best_sellers_category,
    }
    return render(request, "app/index.html", context)


def user_login(request):
    form = CustomUserAuthenticationForm(data=request.POST)
    if form.is_valid():
        email = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
    else:
        print(form.errors)
    return redirect("home")


def user_registration(request):
    form = CustomUserCreationForm(data=request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = form.cleaned_data["email"].split("@")[0]
        user.save()
        return redirect("home")

    return redirect("home")


def user_logout(request):
    logout(request)
    return redirect("home")


def about_view(request):
    gallery_projects = ProjectsGallery.objects.all()
    clients = Client.objects.all()

    context = {"gallery_projects": gallery_projects, "clients": clients}
    return render(request, "app/about.html", context)


def contacts_view(request):
    return render(request, "app/contacts.html")


def sort_products(request, queryset):
    sort_field = request.GET.get("sort")
    if sort_field:
        if sort_field == "price":
            queryset = queryset.order_by("price")
        elif sort_field == "created_at":
            queryset = queryset.order_by("created_at")
        elif sort_field == "name":
            queryset = queryset.order_by("name")
        elif "color" in sort_field:
            queryset = queryset.filter(color=sort_field.split("=")[-1])
        elif "dimming" in sort_field:
            queryset = queryset.filter(dimming=sort_field.split("_")[-1])
        elif "owner" in sort_field:
            queryset = queryset.filter(manufacturer_country=sort_field.split("_")[-1])

    return queryset


def category_detail_view(request, slug):
    category = Category.objects.get(slug=slug)
    qs = Product.objects.filter(category=category)

    category_products = sort_products(request, qs)

    paginator = Paginator(category_products, 2)
    page = request.GET.get("page")
    products = paginator.get_page(page)

    context = {"products": products}
    return render(request, "app/categories.html", context)


def add_comment(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    form = CommentForm(data=request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.product = product
        form.save()
        return redirect("product_detail", product_slug)


def product_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    comments = product.comments.all()

    context = {
        "product": product,
        "form": CommentForm(),
        "comments": comments,
    }
    return render(request, "app/product.html", context)


def to_cart(request, product_id, action):
    product_msg = __make_product_variant_msg(request.POST)
    product = Product.objects.get(pk=product_id)

    obj = MessageTelegram.objects.create(product=product, product_msg=product_msg)
    obj.save()

    if not request.user.is_authenticated:
        session_cart = CartForAnonymousUser(request, product_id, action)
    else:
        user_cart = CartForAuthenticatedUser(request, product_id, action)

    return redirect("cart")


def basket_view(request):
    cart_info = get_cart_data(request)

    print(cart_info)

    if request.method == "POST":
        basket_msg = __make_basket_products_msg(request.POST)
        print(basket_msg)
        for product in cart_info["products"]:
            if request.user.is_authenticated:
                message_tg = MessageTelegram.objects.filter(product_id=product.pk)
            else:
                message_tg = MessageTelegram.objects.filter(product_id=product["pk"])
            print(
                [
                    message_tg_obj.product_msg
                    for message_tg_obj in message_tg
                    if message_tg_obj.product_msg
                ]
            )
            pass

    context = {
        "cart_total_quantity": cart_info["cart_total_quantity"],
        "cart_total_price": cart_info["cart_total_price"],
        "order": cart_info["order"],
        "products": cart_info["products"],
    }
    return render(request, "app/basket.html", context)


def send_phone_number_to_telegram(request):
    phone_number = request.POST.get("phone_number")
    msg = f"""
Оставленный номер телефона: {phone_number}
"""
    req.post(
        settings.CHANNEL_API_LINK.format(
            token=settings.BOT_TOKEN, channel_id=settings.CHANNEL_ID, text=msg
        )
    )

    return redirect("home")
