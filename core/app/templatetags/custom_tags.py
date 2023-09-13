from django import template

from app.models import Category, Product
from app.cart_utils import get_cart_data

register = template.Library()


@register.simple_tag()
def get_cart_total_qty(request):
    cart_data = get_cart_data(request)
    return cart_data["cart_total_quantity"]


@register.simple_tag()
def get_config():
    from constance import config

    return config


@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    return categories


@register.simple_tag()
def is_category_selected(category, path):
    slug_from_path = [item for item in path.split("/") if item][-1]
    return category.slug == slug_from_path


@register.simple_tag()
def is_page_sorted(sort_field, request):
    return sort_field == request.GET.get("sort")


@register.simple_tag()
def get_unique_elements(sort_field):
    result = []
    products = Product.objects.all()
    for product in products:
        if sort_field == "color":
            if product.color not in result:
                result.append(product.color)
        if sort_field == "dimming":
            if product.dimming not in result:
                result.append(product.dimming)
        if sort_field == "manufacturer":
            if product.manufacturer_country not in result:
                result.append(product.manufacturer_country)
    return result


@register.simple_tag()
def convert_price(product: Product):
    import requests

    API_KEY = "0a1fb85a88eafb2934c0bae7"

    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    resp = requests.get(url).json()

    uzs = resp["conversion_rates"]["UZS"]
    price = f"{round(product.price * uzs):,d}".replace(",", " ")
    return price
