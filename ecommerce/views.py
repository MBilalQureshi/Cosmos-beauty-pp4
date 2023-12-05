from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from .models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
import decimal
from django.db.models import Q, F
from .forms import ShipmentDetailForm, ConfirmedOrderDetailForm
import random
from django.contrib import messages
from django.http import JsonResponse


class Home (generic.TemplateView):
    """
    Renders the index page
    """
    template_name = 'index.html'


class ProductSearch(generic.ListView):
    """
    Reders the user search for products by name
    """
    model = Product
    template_name = 'products.html'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('search-product')
        return Product.objects.filter(available=True).filter(
            name__icontains=query).order_by('-created_on')


class Products (generic.ListView):
    """
    Fetch products data from database and display on
    products.html
    """
    queryset = Product.objects.filter(available=True).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 8


class ProductsCategory (generic.ListView):
    """
    Display products based on categories
    """
    queryset = Product.objects.filter(available=True).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        category_param = self.kwargs.get("category")
        category = ProductCategories.objects.get(category_name=category_param)
        products = Product.objects.filter(product_category=category).filter(
            available=True).order_by('-created_on')
        return {'product_list': products}


class SpecialOffers (generic.ListView):
    """
    Display products on special offers
    """
    queryset = Product.objects.filter(available=True).filter(
        stock__gt=0).filter(~Q(discount_name=2)).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 8


class ProductDetail(generic.DetailView):
    """
    Display product details
    """
    def get(self, request, slug, *args, **kwargs):
        queryset = Product.objects.filter(
            slug=slug).order_by('-created_on')
        product = get_object_or_404(queryset)

        discount = 0
        if product.discount_name.discount_percentage > 0:
            discount = (float(product.discount_name.discount_percentage)
                        * float(product.price)) / 100
            discount = product.price-decimal.Decimal(discount)

        product_wish = False
        add_to_cart = False
        if request.user.is_authenticated:
            if Wishes.objects.filter(user=request.user, wish_id=product.id):
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
                'add_to_cart': add_to_cart,
                'discount': discount,
            },
        )


class Wishlist(generic.ListView):
    """
    Display user products in wishlist once logged in
    """
    paginate_by = 8
    template_name = 'wishlist.html'
    context_object_name = 'wishlist'

    def get_queryset(self):
        return Wishes.objects.filter(user=self.request.user)


class AddToWishlist(View):
    """
    Add / remove items to wishlist modal without page refresh
    """
    def post(self, request):
        if request.method == 'POST':
            if request.user.is_authenticated:
                prod_id = int(request.POST.get('productId'))
                product_check = Product.objects.get(id=prod_id)
                if product_check:
                    if Wishes.objects.filter(
                         user=request.user, wish_id=prod_id):
                        wish_delete = get_object_or_404(
                            Wishes, user=request.user, wish_id=prod_id)
                        wish_delete.delete()
                    else:
                        Wishes.objects.create(
                            user=request.user, wish_id=prod_id)
        return redirect('/')


def cart(request):
    """
    Display cart items and total based on cart products
    """
    if request.method == 'POST':
        cart = request.session.get(settings.CART_SESSION_ID)
        request.session.cart = cart
        prod_id = str(request.POST.get('productId'))
        del request.session.cart[prod_id]
        request.session.modified = True
        return redirect('/')
    total = 0.00
    ship_total = 5.00
    if request.session.get('cart') is not None and request.session.get('cart'):
        ids = []

        for key, value in request.session.get('cart').items():
            total += value['prod_total']
            ids.append(str(key))

        products = Product.objects.filter(available=True).filter(
            stock__gt=0).filter(id__in=ids)
        ship_total = round(ship_total + total, 2)
    else:
        products = []
        cart = 'Nothing in cart'
    context = {
        'products': products,
        'total': round(total, 2),
        'ship_total': ship_total,
    }
    return render(request, 'cart.html', context)


class AddToCart(View):
    """
    Add / remove cart items from cart session without page refresh
    items in session are product id, quantity, price, discount, and its total
    """
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
            prod_total = round(prod_total, 2)
            self.session = request.session
            cart = self.session.get(settings.CART_SESSION_ID)
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart
            if prod_id not in self.cart:
                self.cart[prod_id] = {
                    'quantity': prod_quantity,
                    'price': product_price,
                    'discount': prod_discount,
                    'prod_total': prod_total,
                }
            else:
                del self.cart[prod_id]
            request.session.modified = True
            return redirect('/')
        else:
            return redirect('/')


class Checkout(View):
    """
    Shipment details are fetched if already exists, else
    show empty form for user to fill
    """
    def get(self, request):
        if request.user.is_authenticated:
            get_user_last_data = ShipmentDetail.objects.filter(
                user=request.user)
            if get_user_last_data:
                instance = get_object_or_404(
                    get_user_last_data, user=request.user)
                form = ShipmentDetailForm(instance=instance)
            else:
                form = ShipmentDetailForm()
        return render(
            request,
            "user_checkout.html",
            {
                'form': form,
            },
        )

    def post(self, request):
        """
        Update the Shipment detail modal form if needed else forward it as it
        is and add new order data to Confirmed Order Detail and user bill
        modals with invoice number.
        """
        if request.user.is_authenticated:
            get_user_last_data = ShipmentDetail.objects.filter(
                user=request.user)
            if request.session.get('cart'):
                if get_user_last_data:
                    instance = get_object_or_404(ShipmentDetail,
                                                 user=request.user)
                    form = ShipmentDetailForm(request.POST, instance=instance)
                    if form.is_valid():
                        fetch_user = form.save(commit=False)
                        fetch_user.user = request.user
                        messages.success(request,
                                         'Shipment data set successfully')
                        form.save()
                    else:
                        return redirect('checkout')
                else:
                    form = ShipmentDetailForm(request.POST)
                    if form.is_valid():
                        fetch_user = form.save(commit=False)
                        fetch_user.user = request.user
                        messages.success(request,
                                         'Shipment data added successfully')
                        form.save()
                    else:
                        return redirect('checkout')
            else:
                messages.success(self.request, 'Order Already placed')
                return redirect('myorders')
            overall_total = 0.00
            invoice_no = generate_invoice_number()

            if not request.session.get('cart'):
                messages.success(self.request, 'Order Already placed')
                return redirect('myorders')
            else:
                for key, value in request.session.get('cart').items():
                    overall_total += value['prod_total']
                    prod_id = Product.objects.get(id=key)
                    product_quantity_update = Product.objects.filter(
                        id=key).update(stock=F('stock') - value['quantity'])
                    add_confirmed_order = ConfirmedOrderDetail(
                        user_info=request.user,
                        product_info=prod_id,
                        quantity=value['quantity'],
                        prod_total=value['prod_total'],
                        user_unique_order_no=invoice_no
                        )
                    add_confirmed_order.save()

            overall_total = round(5.00 + overall_total, 2)
            user_shipment_id = ShipmentDetail.objects.get(user=request.user)
            user_bill_ref = UserBill(
                user_info=request.user,
                shipment_info=user_shipment_id,
                total=overall_total,
                user_unique_order_no=invoice_no
                )
            user_bill_ref.save()
            messages.success(request, 'Order placed sucessfully')
            del request.session['cart']

        return render(
            request,
            "order_complete.html",
            {
                'form': form,
            },
        )


def generate_invoice_number():
    """
    This function generate random invoice number based on
    the fact that it does't already exist in modal for new
    orders
    """
    is_not_unique = True
    while is_not_unique:
        invoice_no_ref = random.randint(1000000000, 9999999999)
        if not ConfirmedOrderDetail.objects.filter(
             user_unique_order_no=invoice_no_ref):
            is_not_unique = False
    return str(invoice_no_ref)


class MyOrders(View):
    """
    This View show the users orders in my orders user can also update the
    quantity of product based on need.
    Note: Parts of Get function is modified using chat gpt due to an issue
    where form and products data couldn't be zipped togther as list.
    kindly see Testing.md bug#4 for more details.
    """
    def get(self, request):
        get_products = {}
        form_instances = []
        if request.user.is_authenticated:
            get_invoice_list = UserBill.objects.filter(
                user_info=request.user).values_list(
                    'user_unique_order_no', flat=True)
            if get_invoice_list:
                for invoice_number in get_invoice_list:
                    products_data = ConfirmedOrderDetail.objects.filter(
                        user_unique_order_no=invoice_number).values_list(
                            'product_info',
                            'product_info__image',
                            'product_info__name',
                            'quantity', 'prod_total',
                            'product_info__stock',
                            )
                    form_instances_for_invoice = []
                    for product_data in products_data:
                        instance = get_object_or_404(
                            ConfirmedOrderDetail,
                            user_unique_order_no=invoice_number,
                            product_info=product_data[0]
                            )
                        form = ConfirmedOrderDetailForm(instance=instance)
                        form_instances_for_invoice.append(form)
                    get_products[invoice_number] = {
                        'product_info': products_data,
                        'form_instances': form_instances_for_invoice,
                    }
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
            confirmed_product_id = request.POST['product_instance_id']
            product_id = ConfirmedOrderDetail.objects.get(
                id=confirmed_product_id).product_info.id
            product_total = Product.objects.get(
                id=product_id).discount_name.discount_percentage
            discount = 0
            queryset = Product.objects.filter(
                id=product_id).order_by('-created_on')
            product = get_object_or_404(queryset)
            if product.discount_name.discount_percentage > 0:
                discount = (float(product.discount_name.discount_percentage)
                            * float(product.price)) / 100
                discount = product.price-decimal.Decimal(discount)
            else:
                discount = product.price
            new_total = float(quantity) * float(discount)
            instance = get_object_or_404(
                ConfirmedOrderDetail, id=confirmed_product_id)
            form = ConfirmedOrderDetailForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                ConfirmedOrderDetail.objects.filter(
                    id=confirmed_product_id).update(prod_total=round(
                        new_total, 2))
                messages.success(request, 'Quantity updated sucessfully')
            return redirect('myorders')
        return self.get(request)


def delete_order(request, product_key):
    """
    This view cancels the orders
    """
    order_detail = ConfirmedOrderDetail.objects.filter(
        user_unique_order_no=product_key)
    user_bill = UserBill.objects.filter(user_unique_order_no=product_key)
    order_detail.delete()
    user_bill.delete()
    messages.success(request, 'Order cancelled sucessfully')
    return redirect('myorders')


def remove_product(request, product_key, total, prod_id):
    """
    This view remove products from orders
    """
    item = UserBill.objects.filter(
        user_unique_order_no=product_key).values_list(
            'total', flat=True)
    update_total = float(item[0]) - float(total)
    update_user_bill = UserBill.objects.filter(
        user_unique_order_no=product_key).update(total=update_total)
    order_detail = ConfirmedOrderDetail.objects.filter(
        user_unique_order_no=product_key).filter(product_info__id=prod_id)
    order_detail.delete()
    messages.success(request, 'Item removed sucessfully')
    return redirect('myorders')
