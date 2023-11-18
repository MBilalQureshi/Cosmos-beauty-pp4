from django.contrib import admin
from django.contrib.auth.models import User
from .models import ShipmentDetail, ProductCategories, ProductDiscount, Product, ConfirmedOrderDetail, Wishes, UserBill
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
# admin.site.register(ShipmentDetail)
# admin.site.register(UserPayment)
# admin.site.register(ProductCategories)
# admin.site.register(ProductDiscount)
# admin.site.register(Product)
# admin.site.register(CartItem)
# admin.site.register(ConfirmedOrderDetail)


@admin.register(ShipmentDetail)
class ShipmentDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line_one', 'city', 'created_on', 'updated_on')
    search_fields = ('address_line_one', 'mobile', 'city')
    list_filter = ('user', 'created_on')


# @admin.register(UserPayment)
# class UserPaymentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'method', 'created_on', 'updated_on')
#     search_fields = ('user', 'method')
#     list_filter = ('user', 'created_on')


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
    list_display = ('name', 'available', 'stock','product_category', 'price', 'slug')
    search_fields = ('name', 'sku')
    list_filter = ('name', 'created_on', 'updated_on')
    summernote_fields = ('description')
    # prepopulated_fields = {'slug': ('name',)}


# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('user_info', 'product_info', 'quantity','created_on')
#     search_fields = ('user_info', 'product_info')
#     list_filter = ('user_info', 'created_on', 'updated_on')


@admin.register(ConfirmedOrderDetail)
class ConfirmedOrderDetailAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'product_info','quantity', 'order_status','user_unique_order_no')
    search_fields = ('user_info','product_info' ,'quantity')
    list_filter = ('user_info', 'product_info','quantity','user_unique_order_no', 'created_on')

@admin.register(Wishes)
class WishesAdmin(admin.ModelAdmin):
    list_display = ('wish', 'created_on', 'updated_on')
    search_fields = ('wish', 'created_on')
    list_filter = ('wish', 'created_on', 'updated_on')

UserBill
@admin.register(UserBill)
class UserBillAdmin(admin.ModelAdmin):
    list_display = ('user_info','shipment_info', 'user_unique_order_no')
    search_fields = ('user_info','shipment_info','user_unique_order_no')
    list_filter = ('user_info','shipment_info', 'user_unique_order_no')