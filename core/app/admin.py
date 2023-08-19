from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, ProductOption, Product, ProductImage, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk", "name")
    prepopulated_fields = {"slug": ("name",)}


class ProductOptionAdmin(admin.TabularInline):
    model = ProductOption
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductOptionAdmin, ProductImageInline]
