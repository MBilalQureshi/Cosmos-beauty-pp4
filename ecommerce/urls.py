from . import views
from django.urls import path

# app_name = 'products'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('products/', views.Products.as_view(), name='products'),
    path('makeup/', views.Makeup.as_view(), name='makeup'),
    path('skincare/', views.SkinCare.as_view(), name='skincare'),
    path('fragrence/', views.Fragrence.as_view(), name='fragrence'),
    path('bathandbody/', views.BathAndbody.as_view(), name='bathandbody'),
    path('hair/', views.Hair.as_view(), name='hair'),
    path('specialoffers/', views.SpecialOffers.as_view(), name='specialoffers'),
    path('<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
]
