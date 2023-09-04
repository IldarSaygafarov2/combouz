from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .cart_utils import CartForAnonymousUser, CartForAuthenticatedUser, get_cart_data
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm, CommentForm
from .models import Product, Category, ProjectsGallery, Client
from core import settings
import requests as req


def home_view(request):
    gallery_projects = ProjectsGallery.objects.all()
    context = {
        "registration_form": CustomUserCreationForm(),
        "login_form": CustomUserAuthenticationForm(),
        "gallery_projects": gallery_projects
    }
    return render(request, "app/index.html", context)


def user_login(request):
    form = CustomUserAuthenticationForm(data=request.POST)
    if form.is_valid():
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(
            username=email,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('home')
    else:
        print(form.errors)
    return redirect('home')


def user_registration(request):
    form = CustomUserCreationForm(data=request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = form.cleaned_data["email"].split("@")[0]
        user.save()
        return redirect("home")

    return redirect('home')


def user_logout(request):
    logout(request)
    return redirect("home")


def about_view(request):
    gallery_projects = ProjectsGallery.objects.all()
    clients = Client.objects.all()

    context = {
        "gallery_projects": gallery_projects,
        "clients": clients
    }
    return render(request, "app/about.html", context)


def contacts_view(request):
    return render(request, "app/contacts.html")


def sort_products(request, queryset):
    sort_field = request.GET.get('sort')
    if sort_field:
        if sort_field == "price":
            queryset = queryset.order_by('price')
        elif sort_field == 'created_at':
            queryset = queryset.order_by('created_at')
        elif sort_field == 'name':
            queryset = queryset.order_by('name')
        elif 'color' in sort_field:
            queryset = queryset.filter(color=sort_field.split('=')[-1])
        elif 'dimming' in sort_field:
            queryset = queryset.filter(dimming=sort_field.split('_')[-1])
        elif 'owner' in sort_field:
            queryset = queryset.filter(manufacturer_country=sort_field.split('_')[-1])

    return queryset


def category_detail_view(request, slug):
    category = Category.objects.get(slug=slug)
    qs = Product.objects.filter(category=category)

    category_products = sort_products(request, qs)

    paginator = Paginator(category_products, 2)
    page = request.GET.get("page")
    products = paginator.get_page(page)

    context = {
        "products": products
    }
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
    user = request.user.email.split("@")[0]

    product = Product.objects.get(slug=product_slug)
    comments = product.comments.all()

    context = {
        "product": product,
        "form": CommentForm(),
        "comments": comments,
        "username": user
    }
    return render(request, "app/product.html", context)


qd = None


def to_cart(request, product_id, action):
    global qd
    qd = request.POST
    if not request.user.is_authenticated:
        session_cart = CartForAnonymousUser(request, product_id, action)
    else:
        user_cart = CartForAuthenticatedUser(request, product_id, action, query_dict=request.POST)

    return redirect("cart")


def basket_view(request):
    cart_info = get_cart_data(request)
    global qd
    context = {
        "cart_total_quantity": cart_info["cart_total_quantity"],
        "cart_total_price": cart_info["cart_total_price"],
        "order": cart_info["order"],
        "products": cart_info["products"]
    }
    return render(request, "app/basket.html", context)


def send_phone_number_to_telegram(request):
    phone_number = request.POST.get("phone_number")
    msg = f"""
Оставленный номер телефона: {phone_number}
"""
    req.post(
        settings.CHANNEL_API_LINK.format(
            token=settings.BOT_TOKEN,
            channel_id=settings.CHANNEL_ID,
            text=msg
        )
    )

    return redirect('home')