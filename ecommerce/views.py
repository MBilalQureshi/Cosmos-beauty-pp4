from django.shortcuts import render
from django.views import generic, View


# Create your views here.
class Home (generic.TemplateView):
    template_name = 'index.html'


class Products (generic.TemplateView):
    template_name = 'products.html'