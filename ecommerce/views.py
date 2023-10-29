from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Address, UserPayment, ProductCategories, ProductDiscount, Product, CartItems, ConfirmedOrderDetails
from django.utils import timezone

# class a(View):
#     def get_path(self,request):
#         print('hello')
#         current_url = resolve(request.path_info).url_name
#         print(current_url)
# Create your views here.
class Home (generic.TemplateView):
    """
    """
    template_name = 'index.html'


class Products (generic.ListView):
#     def __init__(self, request):
#         urlpath = request.path
    """
    Fetch products data from database and display on
    products.html
    """
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context["url_name"] = resolve(self.request.path_info).url_name
    #     return context
    # fetch url
    # reduce the col required from db from next iteration
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["now"] = timezone.now()
    #     return context


class Makeup (generic.ListView):
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).filter(product_category=2).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12