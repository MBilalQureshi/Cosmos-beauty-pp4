from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Address, UserPayment, ProductCategories, ProductDiscount, Product, CartItems, ConfirmedOrderDetails
from django.utils import timezone


class Home (generic.TemplateView):
    """
    """
    template_name = 'index.html'


class Products (generic.ListView):
    """
    Fetch products data from database and display on
    products.html
    """
    # TASK: CHECK IF DICOUNT EXIST OR NOT
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12


class Makeup (generic.ListView):
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).filter(product_category=2).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12


class SkinCare (generic.ListView):
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).filter(product_category=4).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12


class Hair (generic.ListView):
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).filter(product_category=3).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12


class Fragrence (generic.ListView):
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).filter(product_category=5).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12


class BathAndbody (generic.ListView):
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).filter(product_category=6).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12


class SpecialOffers (generic.ListView):
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).filter(discount_name__gt=1).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12


class ProductDetail(generic.DetailView):
    # queryset = Product.objects.filter(available=True).filter(stock__gt=0).filter(discount_name__gt=1).order_by('-created_on')
    def get(self, request, slug, *args, **kwargs):
        queryset = Product.objects.filter(stock__gt=0).filter(slug=slug).order_by('-created_on')
        product = get_object_or_404(queryset)
    # template_name = 'product_detail.html'
        # accessary_type = ProductCategories.objects.from_queryset()
        return render(
            request,
            "product_detail.html",
            {
                'product': product,
            },
        )