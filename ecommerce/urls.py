from . import views
from django.urls import path

# app_name = 'products'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('products/', views.Products.as_view(), name='products'),
    path('makeup', views.Makeup.as_view(), name='makeup'),
]
