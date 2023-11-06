from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import generic, View
from .models import Address, UserPayment, ProductCategories, ProductDiscount, Product, CartItems, ConfirmedOrderDetails, Wishes
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
from django.conf import settings
import decimal

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
    def get(self, request, slug, *args, **kwargs):
        queryset = Product.objects.filter(stock__gt=0).filter(slug=slug).order_by('-created_on')
        product = get_object_or_404(queryset)
        # check if product is added to wishlist
        # wish_id=product.id ??????????????

        discount = 0
        if product.discount_name.discount_percentage > 0:
            discount = (float(product.discount_name.discount_percentage) * float(product.price)) / 100
            discount = product.price-decimal.Decimal(discount)

        product_wish = False
        if request.user.is_authenticated:
            if(Wishes.objects.filter(user=request.user, wish_id=product.id)):
                print('exist')
                product_wish = True
            else:
                product_wish = False
        return render(
            request,
            "product_detail.html",
            {
                'product': product,
                'product_wish': product_wish,
                'discount':discount,
            },
        )


@login_required(login_url='/accounts/login/')
def wishlist(request):
    wishlist = Wishes.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request, 'wishlist.html',context)

# only adding and removing from wishlist
class AddToWishlist(generic.DetailView):
    def post(self, request):
        if request.method == 'POST':
            if request.user.is_authenticated:
                prod_id = int(request.POST.get('productId'))
                product_check = Product.objects.get(id=prod_id)
                if(product_check):
                    if(Wishes.objects.filter(user=request.user, wish_id=prod_id)):
                        # return JsonResponse('status', 'Product already in wishlist')
                        # remove from wishlist
                        wish_delete = get_object_or_404(Wishes, user=request.user, wish_id=prod_id)
                        wish_delete.delete()
                    else:
                        # add to wish list
                        Wishes.objects.create(user=request.user, wish_id=prod_id)
                else:
                    return JsonResponse('status', 'Login to continue')
        else:
            return JsonResponse({'status', "Login to continue"})
        return redirect('/')


# @login_required(login_url='/accounts/login/')
def cart(request):
    cart = CartItems.objects.filter(user_info=request.user)
    # save cart data from session
    context = {'cart':cart}
    return render(request, 'cart.html',context)


class AddToCart(View):

    def post(self, request):
        if request.method == 'POST':
            prod_id = int(request.POST.get('productId'))
            prod_quantity = int(request.POST.get('productQuantity'))
            if request.user.is_authenticated:
                product_check = Product.objects.get(id=prod_id)
                
                if(product_check):
                    if(CartItems.objects.filter(user_info=request.user, product_info=prod_id)):
                        # remove from wishlist
                        cart_delete = get_object_or_404(CartItems, user_info=request.user, product_info_id=prod_id, quantity=prod_quantity)
                        cart_delete.delete()
                    else:
                        # add to wish list
                        CartItems.objects.create(user_info=request.user, product_info_id=prod_id, quantity=prod_quantity)
            else:


                # request.session[prod_id].insert(0, prod_id)
                # request.session.modified = True
                # print(self.session)

                # print('HELLO')
                self.session = request.session
                cart = self.session.get(settings.CART_SESSION_ID)
                # empty cart saved in session
                if not cart:
                    print('cart empty')
                    cart = self.session[settings.CART_SESSION_ID]={}
                self.cart = cart
                prod_id = str(prod_id)
                if prod_id not in self.cart:
                    print('no delete')
                    self.cart[int(prod_id)]={'quantity':prod_quantity, 'price':str(3)}
                else:
                    print('delete')
                    del self.cart[prod_id]
                # self.session.save()
                request.session.modified = True
                print(self.cart)

                # print(request.session.get(cart['4']['quantity']))
                # session_id = request.session._get_or_create_session_key()
                # response = HttpResponse('sessionID_set')
                # tomorrow = datetime.datetime.now() + datetime.timedelta(days = 1)
                # response.set_cookie('sessionid', session_id, expires=tomorrow)
                # print(session_id)
                
                return redirect('/')

        else:
            return redirect('/')