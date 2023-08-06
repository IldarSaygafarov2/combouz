from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk", "name")
    prepopulated_fields = {"slug": ("name",)}
