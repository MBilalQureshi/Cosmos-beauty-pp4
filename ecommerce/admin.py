from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


@admin.register(ShipmentDetail)
class ShipmentDetailAdmin(admin.ModelAdmin):
    """
    Allows admin to manage Shipment Detail via the admin panel
    """
    list_display = ('user', 'address_line_one', 'city', 'created_on',
                    'updated_on')
    search_fields = ('address_line_one', 'mobile', 'city')
    list_filter = ('user', 'created_on')


@admin.register(ProductCategories)
class ProductCategoriesAdmin(admin.ModelAdmin):
    """
    Allows admin to manage Product Categories 
    via the admin panel
    """
    list_display = ('category_name', 'created_on', 'updated_on')
    search_fields = ('category_name', 'created_on', 'updated_on')
    list_filter = ('category_name', 'created_on', 'updated_on')


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    """
    Allows admin to manage Product Discount via the admin panel
    """
    list_display = ('discount_name', 'discount_percentage', 'active',
                    'created_on')
    search_fields = ('discount_name', 'active')
    list_filter = ('discount_name', 'created_on', 'updated_on')


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    """
    Allows admin to manage Product via the admin panel
    """
    list_display = ('name', 'available', 'stock', 'product_category', 'price',
                    'slug')
    search_fields = ('name', 'sku')
    list_filter = ('name', 'created_on', 'updated_on')
    summernote_fields = ('description')


@admin.register(ConfirmedOrderDetail)
class ConfirmedOrderDetailAdmin(admin.ModelAdmin):
    """
    Allows admin to manage Confirmed Order Detail via the admin panel
    """
    list_display = ('user_info', 'product_info', 'quantity', 'order_status',
                    'user_unique_order_no')
    search_fields = ('user_info', 'product_info', 'quantity')
    list_filter = ('user_info', 'product_info', 'quantity',
                   'user_unique_order_no', 'created_on')


@admin.register(Wishes)
class WishesAdmin(admin.ModelAdmin):
    """
    Allows admin to manage Wishes via the admin panel
    """
    list_display = ('wish', 'created_on', 'updated_on')
    search_fields = ('wish', 'created_on')
    list_filter = ('wish', 'created_on', 'updated_on')


@admin.register(UserBill)
class UserBillAdmin(admin.ModelAdmin):
    """
    Allows admin to manage User Bill via the admin panel
    """
    list_display = ('user_info', 'shipment_info', 'user_unique_order_no')
    search_fields = ('user_info', 'shipment_info', 'user_unique_order_no')
    list_filter = ('user_info', 'shipment_info', 'user_unique_order_no')
