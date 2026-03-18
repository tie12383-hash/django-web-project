from django.core.cache import cache
from .models import Product

def get_products_by_category(category_id):
    """
    Возвращает список опубликованных продуктов в указанной категории.
    Использует низкоуровневое кеширование.
    """
    cache_key = f'category_products_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        # Если нет в кеше, получаем из БД
        products = list(Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).select_related('category').order_by('-created_at'))
        cache.set(cache_key, products, 60 * 15)  # 15 минут
    return products