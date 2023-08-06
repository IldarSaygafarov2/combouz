from django.shortcuts import render, HttpResponse


def home_view(request):
    return render(request, "app/index.html")


def about_view(request):
    return render(request, "app/about.html")


def contacts_view(request):
    return render(request, "app/contacts.html")


def categories_view(request):
    return render(request, "app/categories.html")


def product_view(request, product_slug):
    return render(request, "app/product.html")
