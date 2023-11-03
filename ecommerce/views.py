from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from .models import Address, UserPayment, ProductCategories, ProductDiscount, Product, CartItems, ConfirmedOrderDetails, Wishes
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
        return render(
            request,
            "product_detail.html",
            {
                'product': product,
            },
        )


@login_required(login_url='/accounts/login/')
def WishList(request):
        wishlist = Wishes.objects.filter(user=request.user)
        context = {'wishlist':wishlist}
        return render(request, 'wishlist.html',context)

class AddToWishlist(generic.DetailView):
    def post(self, request):
        if request.method == 'POST':
            print('hey')
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
# class WishList(generic.ListView):
#     queryset = Wishes.objects.all().order_by('-created_on')
#     # wishes = get_object_or_404(queryset)
#     template_name = 'wishlist.html'

    # def get(self, request, slug, *args, **kwargs):
    #     queryset = Wishes.objects.filter(user=request.user)
    #     wishes = get_object_or_404(queryset)
    #     return render(
    #         request,
    #         "wishlist.html",
    #         {
    #             'wishes': wishes,
    #         }
    #     )
# class WishList(View): 
#     def post(self, request, slug, *args, **kwargs):
#         if self.request.POST.get('action') == 'wish':

#             id = int(self.request.POST.get('productId'))
#             button = self.request.POST.get('button')
#             product = Product.objects.get(id=id)

#             print(id)
#         else:
#             print('fuck')