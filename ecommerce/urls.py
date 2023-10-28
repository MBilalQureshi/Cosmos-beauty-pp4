from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('products/', views.Products.as_view(), name='products'),
]
