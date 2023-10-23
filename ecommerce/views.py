from django.shortcuts import render
from django.views import generic, View


# Create your views here.
class Home (generic.TemplateView):
    template_name = 'index.html'
