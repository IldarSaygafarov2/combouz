from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contacts/", views.contacts_view, name="contacts"),
    path("categories/", views.categories_view, name="categories"),
    path("products/<slug:product_slug>/", views.product_view, name="product_detail"),
]
