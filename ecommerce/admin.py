from django.contrib import admin
from django.contrib.auth.models import User
from .models import Address, UserPayment, ProductCategories, ProductDiscount, Product, CartItems, ConfirmedOrderDetails
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
# admin.site.register(Address)
# admin.site.register(UserPayment)
# admin.site.register(ProductCategories)
# admin.site.register(ProductDiscount)
# admin.site.register(Product)
# admin.site.register(CartItems)
# admin.site.register(ConfirmedOrderDetails)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line_one', 'city', 'created_on', 'updated_on')
    search_fields = ('address_line_one', 'mobile', 'city')
    list_filter = ('user', 'created_on')


@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'method', 'created_on', 'updated_on')
    search_fields = ('user', 'method')
    list_filter = ('user', 'created_on')


@admin.register(ProductCategories)
class ProductCategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'created_on', 'updated_on')
    search_fields = ('category_name', 'created_on', 'updated_on')
    list_filter = ('category_name', 'created_on', 'updated_on')


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_name', 'discount_percentage', 'active','created_on')
    search_fields = ('discount_name', 'active')
    list_filter = ('discount_name', 'created_on', 'updated_on')


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    list_display = ('name', 'available', 'stock','product_category', 'discount_name', 'slug')
    search_fields = ('name', 'sku')
    list_filter = ('name', 'created_on', 'updated_on')
    summernote_fields = ('description')
    # prepopulated_fields = {'slug': ('name',)}


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'product_info', 'quantity','created_on')
    search_fields = ('user_info', 'product_info')
    list_filter = ('user_info', 'created_on', 'updated_on')


@admin.register(ConfirmedOrderDetails)
class ConfirmedOrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'total', 'shipment_via','user_payment', 'order_status','created_on')
    search_fields = ('user_info', 'total', 'shipment_via','user_payment',)
    list_filter = ('user_info', 'total', 'shipment_via','user_payment', 'created_on')

