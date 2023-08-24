from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Category,
    ProductOption,
    Product,
    ProductImage,
    CustomUser,
    ProjectsGallery,
    Client
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("pk", "email", "phone_number", "is_staff")
    ordering = ["email"]


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
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProjectsGallery)
class ProjectsGalleryAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass