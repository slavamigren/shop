from django.views.decorators import cache

from catalog.models import ProductVersion
from config import settings


def get_active_products_version():
    """Возвращает активные версии всех продуктов"""
    if settings.CACHE_ENABLED:
        key = 'product_version_list'
        product_version_list = cache.get('key')
        if product_version_list is None:
            product_version_list = ProductVersion.objects.filter(is_actual=True)
            cache.set('key', product_version_list)
    else:
        product_version_list = ProductVersion.objects.filter(is_actual=True)
    return product_version_list
