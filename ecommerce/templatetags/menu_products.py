import datetime
from django import template
from ecommerce.models import ProductCategories


register = template.Library()

@register.inclusion_tag("menu_products.html")
def show_products_menu():
    categories = ProductCategories.objects.all()
    return {"categories": categories}
