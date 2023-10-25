from django.contrib import admin
from .models import Address, UserPayment, ProductCategories, ProductDiscount, Product, CartItems, ConfirmedOrderDetails
# Register your models here.
admin.site.register(Address)
admin.site.register(UserPayment)
admin.site.register(ProductCategories)
admin.site.register(ProductDiscount)
admin.site.register(Product)
admin.site.register(CartItems)
admin.site.register(ConfirmedOrderDetails)
