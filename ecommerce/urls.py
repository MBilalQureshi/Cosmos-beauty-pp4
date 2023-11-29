from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

"""
URL paths
"""
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('search-products', views.ProductSearch.as_view(),
         name='search_products'),
    path('products/<str:category>', views.ProductsCategory.as_view(),
         name='products_category'),
    path('products/', views.Products.as_view(), name='products'),
    path('specialoffers/', views.SpecialOffers.as_view(),
         name='specialoffers'),
    path('wishlist/', login_required(views.Wishlist.as_view()), name='wishlist'),
    path('add-to-wishlist/', views.AddToWishlist.as_view(),
         name='addtowishlist'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/', views.AddToCart.as_view(), name='addtocart'),
    path('checkout/', login_required(views.Checkout.as_view()),
         name='checkout'),
    path('my-orders/', login_required(views.MyOrders.as_view()),
         name='myorders'),
    path('cancel-order/<product_key>', views.delete_order,
         name='cancel-order'),
    path('remove-product/<product_key>/<total>/<prod_id>',
         views.remove_product, name='removeproduct'),
    path('<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
]
