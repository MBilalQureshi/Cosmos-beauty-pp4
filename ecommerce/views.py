from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import generic, View
from .models import Address, UserPayment, ProductCategories, ProductDiscount, Product, CartItems, ConfirmedOrderDetails, Wishes
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
from django.conf import settings
import decimal
from django.db.models import Q
from .forms import AddressForm


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
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).filter(~Q(discount_name = 2)).order_by('-created_on')
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
        add_to_cart = False
        if request.user.is_authenticated:
            if(Wishes.objects.filter(user=request.user, wish_id=product.id)):
                product_wish = True
            else:
                product_wish = False
        if request.session.get('cart') is not None:
            if str(product.id) in request.session.get('cart'):
                add_to_cart = True
            else:
                add_to_cart = False
        return render(
            request,
            "product_detail.html",
            {
                'product': product,
                'product_wish': product_wish,
                'add_to_cart':add_to_cart,
                'discount':discount,
            },
        )


@login_required(login_url='/accounts/login/')
def wishlist(request):
    wishlist = Wishes.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request, 'wishlist.html',context)

# only adding and removing from wishlist
class AddToWishlist(View):
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
    if request.method == 'POST':
        # When in cart remove item from cart
        cart = request.session.get(settings.CART_SESSION_ID)
        request.session.cart = cart
        prod_id = str(request.POST.get('productId'))
        del request.session.cart[prod_id]
        request.session.modified = True
        return redirect('/')
    total = 0.00
    ship_total = 5.00
    if request.session.get('cart') is not None and request.session.get('cart'):
        # cart = request.session.get('cart')
        ids = []
        
        for key,value in request.session.get('cart').items():
            # print("135", request.session.get('cart').items())
            total += value['prod_total']
            print(f'Key: {key}, Value: {value}')

            ids += key
        products = Product.objects.filter(available=True).filter(stock__gt=0).filter(id__in=ids)
        # for i in range(len(products)):
        #     # products[i].append({'quantity':1})
        #     products[i]["quantity"] = 3
        # print(products)
        # for p in products:
        #     print(p)
        total = round(total, 2)
        ship_total = ship_total + total
    else:
        # TASK HANDLE EMPTY CART
        products = []
        cart = 'Nothing in cart'
    context = {'products':products, 'total':total, 'ship_total': ship_total,}
    return render(request, 'cart.html', context)



class AddToCart(View):
    def post(self, request):
        if request.method == 'POST':
            prod_id = str(request.POST.get('productId'))
            prod_quantity = int(request.POST.get('productQuantity'))
            product_price = float(request.POST.get('price'))
            if request.POST.get('discount') is not None:
                prod_discount = float(request.POST.get('discount'))
                prod_total = prod_discount * prod_quantity
            else:
                prod_discount = 0.0
                prod_total = product_price * prod_quantity
            self.session = request.session
            cart = self.session.get(settings.CART_SESSION_ID)
            # empty cart saved in session
            if not cart:
                cart = self.session[settings.CART_SESSION_ID]={}
            self.cart = cart
            # prod_id = int(prod_id)
            if prod_id not in self.cart:
                self.cart[prod_id]={'quantity':prod_quantity, 'price':product_price, 'discount':prod_discount, 'prod_total':prod_total}
            else:
                del self.cart[prod_id]
            request.session.modified = True
            print(self.cart)
            return redirect('/')
    #         request.session.clear()
    # request.session.flush()
        else:
            return redirect('/')


class Checkout(View):
    def get(self, request):
        print('plol')
        if request.user.is_authenticated:
            print('p2')
            form = AddressForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print('invalid form')
            form = AddressForm()
        return render(
            request,
            "user_checkout.html",
            {
                'form': form,
            },
        )

    def post(self, request):
        print('p1')
        queryset = Product.objects.filter(stock__gt=0).order_by('-created_on')
        if request.user.is_authenticated:
            print('p2')
            form = AddressForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print('invalid form')
            form = AddressForm()
            # check if current user address, name, email exist show them in box and ask if need to edit also shipping method

        return render(
            request,
            "user_checkout.html",
            {
                'form': form,
            },
        )

    