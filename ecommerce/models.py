from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator
from autoslug import AutoSlugField
from phone_field import PhoneField

# Address modal
class ShipmentDetail(models.Model):
    """User Payment Modal"""
    PAYMENT_METHOD_CHOICES = [
        (0, "COD(Cash on delivery)"),
        # (1, "Credit Card"),
        # (2, "Debit Card"),
        # (3, "Paypal"),
        # (4, "Sofort by Klarna"),
        # (5, "Google Pay"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_address")
    first_name = models.CharField(max_length=30,null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    address_line_one = models.CharField(max_length=300, null=False, blank=False)
    postal_code = models.IntegerField(null=False, blank=False)
    city = models.CharField(max_length=250, null=False,blank=False)
    country = models.CharField(max_length=250, null=False,blank=False)
    telephone = PhoneField(null=True, blank=True, unique=False)
    mobile = PhoneField(max_length=14, null=False, blank=False, unique=True)
    method = models.IntegerField(choices=PAYMENT_METHOD_CHOICES, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# class UserPayment(models.Model):
#     """User Payment Modal"""
#     PAYMENT_METHOD_CHOICES = [
#         (0, "COD(Cash on delivery)"),
#         (1, "Credit Card"),
#         (2, "Debit Card"),
#         (3, "Paypal"),
#         (4, "Sofort by Klarna"),
#         (5, "Google Pay"),
#     ]
#     method = models.IntegerField(choices=PAYMENT_METHOD_CHOICES, default=0)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_payment")
#     acc_no = models.IntegerField(null=True, blank=True)
#     expiry = models.DateField(null=True, blank=True)
#     amount = models.IntegerField(null=False, blank=False,default=0)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.first_name} {self.user.last_name}"


class ProductCategories(models.Model):
    category_name = models.CharField(max_length=150, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        # ordering = ['created_on']

    def __str__(self):
        return self.category_name


class ProductDiscount(models.Model):
    discount_name = models.CharField(max_length=150, blank=False)
    discount_percentage = models.PositiveIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.discount_name


class Product(models.Model):
    sku = models.CharField(max_length=16, blank=True)
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    image = CloudinaryField('image', default='placeholder')
    available = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0, null=False)
    product_category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE, related_name="product_category")
    discount_name = models.ForeignKey(ProductDiscount, default=1, on_delete=models.SET_DEFAULT, related_name="product_discount")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    # popularproduct based on most bought products

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user_info = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_info")
    product_info = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="user_product_info")
    # sessionId = 
    quantity = models.PositiveIntegerField(blank=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(10)
    ])
    # TASK SEE LATER IF EXTRA INFO NEEDE BASIC INTENTION WAS FROM FRANGRENCE ML
    extra_info = models.CharField(max_length=250, blank=True, default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user_info.first_name} {self.user_info.last_name}"


class ConfirmedOrderDetail(models.Model):
    SHIPMENT_VIA = [
        (0, 'DHL'),
        (1, 'Hermes'),
        (3, 'DPD')
    ]
    user_info = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_confirmed_order")
    total = models.DecimalField(max_digits=6, decimal_places=2)
    shipment_via = models.IntegerField(choices=SHIPMENT_VIA, default=0)
    # user_payment = models.OneToOneField(UserPayment, on_delete=models.PROTECT, related_name="user_payment_method")
    order_status = models.CharField(max_length=50, default="Order Received")
    # slug = AutoSlugField(populate_from='user_info', unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user_info.first_name} {self.user_info.last_name}"


# only when user is authenticated
class Wishes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userid")
    wish = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="user_wish")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
        

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Wishes'

    # def __str__(self):
    #     return f"{self.user_info.first_name} {self.user_info.last_name}"