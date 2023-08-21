from django import template

from app.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    return categories


@register.simple_tag()
def is_category_selected(category, path):
    slug_from_path = [item for item in path.split('/') if item][-1]
    return category.slug == slug_from_path
