from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Address modal
class Address(models.Model):
    address_line_one = models.CharField(max_length=300, null=False, blank=False)
    postal_code = models.IntegerField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_address")
    city = models.CharField(max_length=250, null=False,blank=False)
    country = models.CharField(max_length=250, null=False,blank=False)
    telephone = models.IntegerField(null=True, blank=True)
    mobile = models.IntegerField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class UserPaymnet(models.Model):
    """User Payment Modal"""
    PAYMENT_METHOD_CHOICES = [
        (0, "COD(Cash on delivery)"),
        (1, "Credit Card"),
        (2, "Debit Card"),
        (3, "Paypal"),
        (4, "Sofort by Klarna"),
        (5, "Google Pay"),
    ]
    method = models.IntegerField(choices=PAYMENT_METHOD_CHOICES, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_payment")
    acc_no = models.IntegerField(null=True, blank=True)
    expiry = models.DateField(null=True, blank=True)
    amount = models.IntegerField(null=False, blank=False,default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"