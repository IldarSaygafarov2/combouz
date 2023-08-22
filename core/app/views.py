from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm
from .models import Product, Category, ProjectsGallery, Client, CustomUser


def home_view(request):
    print('asd')
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            # print(obj)
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    gallery_projects = ProjectsGallery.objects.all()

    context = {
        "form": form,
        "gallery_projects": gallery_projects
    }
    return render(request, "app/index.html", context)


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


def categories_view(request):
    return render(request, "app/categories.html")


def category_detail_view(request, slug):
    category = Category.objects.get(slug=slug)
    category_products = Product.objects.filter(category=category)
    context = {
        "products": category_products
    }
    return render(request, "app/categories.html", context)


def product_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    context = {
        "product": product
    }
    return render(request, "app/product.html", context)


def basket_view(request):
    return render(request, "app/basket.html")
