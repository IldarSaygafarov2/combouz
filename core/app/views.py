from django.shortcuts import render, HttpResponse
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm


def home_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm()

    context = {
        "form": form
    }
    return render(request, "app/index.html", context)


def about_view(request):
    return render(request, "app/about.html")


def contacts_view(request):
    return render(request, "app/contacts.html")


def categories_view(request):
    return render(request, "app/categories.html")


def category_detail_view(request, slug):
    return render(request, "app/categories.html")


def product_view(request, product_slug):
    return render(request, "app/product.html")


def basket_view(request):
    return render(request, "app/basket.html")
