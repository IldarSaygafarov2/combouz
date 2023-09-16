from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contacts/", views.contacts_view, name="contacts"),
    path("categories/<slug:slug>/", views.category_detail_view, name="category_detail"),
    path("products/<slug:product_slug>/", views.product_view, name="product_detail"),
    path("cart/", views.basket_view, name="cart"),
    path('users/register/', views.user_registration, name="register"),
    path('users/login/', views.user_login, name="login"),
    path('users/logout/', views.user_logout, name="logout"),
    path("to_cart/<int:product_id>/<str:action>/", views.to_cart, name="to_cart"),
    path("send_email/", views.send_phone_number_to_telegram, name="send_email"),
]
