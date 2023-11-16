from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import generic, View
from .models import ShipmentDetail, ProductCategories, ProductDiscount, Product, CartItem, ConfirmedOrderDetail, Wishes, UserBill
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
from django.conf import settings
import decimal
from django.db.models import Q
from .forms import ShipmentDetailForm, ConfirmedOrderDetailForm
import random
from django.contrib import messages


class Home (generic.TemplateView):
    """
    """
    template_name = 'index.html'

class ProductSearch(generic.ListView):
    model = Product
    template_name = 'products.html'
    paginate_by = 12
    def get_queryset(self):
        query = self.request.GET.get('search-product')
        return  Product.objects.filter(available=True).filter(stock__gt=0).filter(name__icontains=query).order_by('-created_on')

class Products (generic.ListView):
    """
    Fetch products data from database and display on
    products.html
    """
    # TASK: CHECK IF DICOUNT EXIST OR NOT
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12


class ProductsCategory (generic.ListView):
    """
    Fetch products data from database and display on
    products.html
    """
    # TASK: CHECK IF DICOUNT EXIST OR NOT
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        category_param = self.kwargs.get("category")
        category = ProductCategories.objects.get(category_name=category_param)
        products =  Product.objects.filter(product_category=category).filter(available=True).filter(stock__gt=0).order_by('-created_on')
        return {'product_list': products}


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
        print(total)
        ship_total = round(ship_total + total,2)
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
            prod_total = round(prod_total,2)
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
        if request.user.is_authenticated:
            # get user data if avalable
            get_user_last_data = ShipmentDetail.objects.filter(user=request.user)
            if get_user_last_data:
                instance = get_object_or_404(get_user_last_data, user=request.user)
                # print(instance.first_name)
                form = ShipmentDetailForm(instance = instance)
            else:
                # set to empty form if data not available
                form = ShipmentDetailForm()
        return render(
            request,
            "user_checkout.html",
            {
                'form': form,
            },
        )

    def post(self, request):
        # if request.user.is_authenticated:
        #     get_user_last_data = ShipmentDetail.objects.filter(user=request.user)
        #     if get_user_last_data:
        #         # update form
        #         instance = get_object_or_404(ShipmentDetail, user=request.user)
        #         form = ShipmentDetailForm(request.POST,instance = instance)
        #         if form.is_valid():
        #             fetch_user = form.save(commit=False)
        #             fetch_user.user = request.user
        #             form.save()
        #             messages.success(request, 'Shipment details updated successfully.')
        #         else:
        #             messages.error(request, 'Error updating Shipment details.')
        #             return redirect('checkout')
        #     else:
        #         # First time add form
        #         form = ShipmentDetailForm(request.POST)
        #         if form.is_valid():
        #             fetch_user = form.save(commit=False)
        #             fetch_user.user = request.user
        #             form.save()
        #             # messages.success(request, 'Shipment details added successfully.')
        #         else:
        #             messages.error(request, 'Error adding Shipment details.')
        #             return redirect('checkout')

        #     overall_total = 0.00
        #     invoice_no = create_new_ref_number()
        #     print(invoice_no)
        #     # TASK UPDATE THE QUANTITY IN PRODUCTS STOCK
            
        #     if not request.session.get('cart'):
        #         messages.error(request, 'Order already submitted.')
        #         return redirect('myorders')
        #     else:
        #         for key,value in request.session.get('cart').items():
        #         # print("135", request.session.get('cart').items())
        #             # print(f'Key: {key}, Value: {value}')
        #             overall_total += value['prod_total']
        #             prod_id = Product.objects.get(id=key)
        #             add_confirmed_order = ConfirmedOrderDetail(user_info=request.user, product_info=prod_id, quantity=value['quantity'],prod_total = value['prod_total'],user_unique_order_no=invoice_no)
        #             add_confirmed_order.save()
            
        #     overall_total = round(5.00 + overall_total,2)
        #     user_shipment_id = ShipmentDetail.objects.get(user=request.user)
        #     user_bill_ref = UserBill(user_info=request.user,shipment_info= user_shipment_id ,total=overall_total,user_unique_order_no=invoice_no)
        #     user_bill_ref.save()
        #     del request.session['cart']
            
        return render(
            request,
            "order_complete.html",
            {
                # 'form': form,
            },
        )
        # return self.get(request)

def create_new_ref_number():
    not_unique = True
    while not_unique:
        unique_ref = random.randint(1000000000, 9999999999)
        if not ConfirmedOrderDetail.objects.filter(user_unique_order_no=unique_ref):
            not_unique = False
    return str(unique_ref)

class MyOrders(View):
    def get(self, request):
        get_products = {}
        form_instances = []

        if request.user.is_authenticated:
            # get user invoices
            get_invoice_list = UserBill.objects.filter(user_info=request.user).values_list('user_unique_order_no', flat=True)

            if get_invoice_list:
                for invoice_number in get_invoice_list:
                    # get products data based on invoice numbers
                    products_data = ConfirmedOrderDetail.objects.filter(user_unique_order_no=invoice_number).values_list('product_info', 'product_info__image', 'product_info__name', 'quantity', 'prod_total', 'product_info__stock',)
                    
                    form_instances_for_invoice = []  # Store form instances for each invoice
                    
                    for product_data in products_data:
                        instance = get_object_or_404(ConfirmedOrderDetail, user_unique_order_no=invoice_number, product_info=product_data[0])
                        form = ConfirmedOrderDetailForm(instance=instance)
                        form_instances_for_invoice.append(form)

                    # Store product data and form instances in the dictionary
                    get_products[invoice_number] = {
                        'product_info': products_data,
                        'form_instances': form_instances_for_invoice,
                    }

                    # Extend the list of all form instances
                    form_instances.extend(form_instances_for_invoice)

        return render(
            request,
            "my_orders.html",
            {
                'get_products': get_products,
                'form_instances': form_instances,
            },
        )

    def post(self, request):
        if 'quantity' in request.POST:
            quantity = request.POST['quantity']
            product_id = request.POST['product_instance_id']    

            instance = get_object_or_404(ConfirmedOrderDetail, id=product_id)
            
            form = ConfirmedOrderDetailForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Quantity updated successfully.')
            else:
                messages.error(request, 'Error updating quantity.')

            return redirect('myorders')
        else:
            messages.error(request, 'Cannot update quantity.')
        return self.get(request)

def delete_order(request, product_key):
    # Handle stock
    order_detail = ConfirmedOrderDetail.objects.filter(user_unique_order_no=product_key)
    user_bill = UserBill.objects.filter(user_unique_order_no=product_key)
    order_detail.delete()
    user_bill.delete()
    messages.success(request, 'Order cancelled successfully.')
    return redirect('myorders')

def remove_product(request, product_key, total, prod_id):
    # Handle stock
    item = UserBill.objects.filter(user_unique_order_no=product_key).values_list('total', flat=True)
    update_total = float(item[0]) - float(total)
    update_user_bill = UserBill.objects.filter(user_unique_order_no=product_key).update(total = update_total)
    order_detail = ConfirmedOrderDetail.objects.filter(user_unique_order_no=product_key).filter(product_info__id = prod_id)
    order_detail.delete()
    messages.success(request, 'Product removed successfully.')
    return redirect('myorders')