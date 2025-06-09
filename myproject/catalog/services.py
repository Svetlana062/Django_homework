from .models import Product

def get_products_by_category(category_id):
    """Возвращает список продуктов в указанной категории."""
    return Product.objects.filter(category_id=category_id, status='published')
