from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Address, UserPayment, ProductCategories, ProductDiscount, Product, CartItems, ConfirmedOrderDetails


# Create your views here.
class Home (generic.TemplateView):
    """
    """
    template_name = 'index.html'


class Products (generic.ListView):
    """
    Fetch products data from database and display on
    products.html
    """
    model = Product
    # reduce the col required from db from next iteration
    queryset = Product.objects.filter(available=True).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12

    #  # Dropdown menu list
    # cat_list = Category.objects.all()
    # cat_list_view = Category.objects.all().values("title", "image")