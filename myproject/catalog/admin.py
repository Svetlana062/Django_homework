from django.contrib import admin
from .models import Product, Category

class CategoryAdmin(admin.ModelAdmin):
    """Класс для отображения модели Category в админке."""
    list_display = ('id', 'name')

class ProductAdmin(admin.ModelAdmin):
    """Класс для отображения модели Product в админке."""
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
