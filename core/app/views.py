import requests as req
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from core import settings
from .cart_utils import CartForAnonymousUser, CartForAuthenticatedUser, get_cart_data
from .forms import CustomUserAuthenticationForm, CustomUserCreationForm
from .models import (
    FAQ,
    Category,
    Client,
    Feedback,
    MessageTelegram,
    Product,
    ProjectsGallery, Comment, CommentItem,
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

ITEM_CONTROLS = {
    "left": "Слева",
    "right": "Справа",
}


def __make_product_variant_msg(product_data, product_name=""):
    if not product_data:
        return

    item_control = product_data.get('item-control')
    item_cornice_type = product_data.get('item-cornice-type')
    item_control_type = product_data.get('item-control-type')

    return f"""
Название продукта: {product_name}
Ширина: {product_data['item-width']}
Длина: {product_data['item-length']}
Управление: {ITEM_CONTROLS[item_control] if item_control else '-'}
Кол-во: {product_data['item-count']}
Тип карниза: {CORNICE_TYPES[item_cornice_type] if item_cornice_type else '-'}
Тип управления: {CONTROL_TYPES[item_control_type] if item_control_type else '-'}
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


def product_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    sort = request.GET.get('sort')

    if sort:
        return redirect(f"/categories/{product.category.slug}/?sort={sort}")

    next_num = request.GET.get('next')
    comments_total = product.comments.count()
    comments = product.comments.all()[0:2]

    if next_num:
        next_num = int(next_num)
        comments = product.comments.all()[:next_num + next_num]

    if request.method == "POST":
        data = request.POST
        images = request.FILES.getlist('img')

        comment = Comment.objects.create(
            author=request.user,
            product=product,
            body=data['body']
        )
        comment.save()

        for image in images:
            comment_item = CommentItem.objects.create(
                comment=comment,
                img=image
            )
            comment_item.save()
        return redirect("product_detail", product_slug=product_slug)

    context = {
        "product": product,
        "comments": comments,
        "comments_total": comments_total
    }
    return render(request, "app/product.html", context)


def to_cart(request, product_id, action):
    product = Product.objects.get(pk=product_id)
    product_msg = __make_product_variant_msg(request.POST)

    obj = MessageTelegram.objects.create(product=product, product_msg=product_msg)
    obj.save()

    if not request.user.is_authenticated:
        session_cart = CartForAnonymousUser(request, product_id, action)
    else:
        user_cart = CartForAuthenticatedUser(request, product_id, action)

    return redirect("cart")


def basket_view(request):
    cart_info = get_cart_data(request)

    if request.method == "POST":
        basket_msg = __make_basket_products_msg(request.POST)

        for product in cart_info["products"]:
            if request.user.is_authenticated:
                message_tg = MessageTelegram.objects.filter(product_id=product.product.pk)
            else:
                message_tg = MessageTelegram.objects.filter(product_id=product["pk"])

            basket_msg += ''.join([
                message_tg_obj.product_msg
                for message_tg_obj in message_tg
                if message_tg_obj.product_msg
            ])

            basket_msg += f"Продукт: {product.product.name}"
            req.post(
                settings.CHANNEL_API_LINK.format(
                    token=settings.BOT_TOKEN,
                    channel_id=settings.CHANNEL_ID,
                    text=basket_msg
                )
            )

    category = cart_info['products'].last()
    category = category.product.category if category else None
    last_product = cart_info['products'].last().product if category else None
    context = {
        "cart_total_quantity": cart_info["cart_total_quantity"],
        "cart_total_price": cart_info["cart_total_price"],
        "order": cart_info["order"],
        "products": cart_info["products"],
        "category": category,
        "last_product": last_product,
    }
    return render(request, "app/basket.html", context)


def send_phone_number_to_telegram(request):
    phone_number = request.POST.get("phone_number")
    msg = f"Оставленный номер телефона: {phone_number}"
    req.post(
        settings.CHANNEL_API_LINK.format(
            token=settings.BOT_TOKEN,
            channel_id=settings.CHANNEL_ID,
            text=msg
        )
    )

    return redirect("home")
