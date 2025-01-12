from django.contrib import admin
from .models import EmallsShop, Product


@admin.register(EmallsShop)
class EmallsShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'price']
    search_fields = ['name', 'url', 'price']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'image_url', 'store_count', 'price', 'product_id']
    search_fields = ['name', 'url', 'image_url', 'store_count', 'price', 'product_id']
