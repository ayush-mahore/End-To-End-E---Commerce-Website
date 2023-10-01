from django.shortcuts import render, redirect
from django.views import View
from App.models import Customer, Product, Cart, OrderPlaced
from App.forms import CustomerRegistraionForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        totalitems = 0
        topwears = Product.objects.filter(category='TW')
        bottemwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        return render(request, 'home.html', {'topwears': topwears, 'bottemwears': bottemwears,
                                             'mobiles': mobiles, 'laptops': laptops, 'totalitems': totalitems})


class ProductDetailView(View):
    def get(self, request, pk):
        totalitems = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitems': totalitems})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    Cart(user=user, product_id=product_id).save()

    return redirect('/show_cart')


@login_required
def show_cart(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp = (p.quantity * p.product.discount_price)
                amount += temp
                total_amount = amount + shipping_amount
    return render(request, 'addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount, 'totalitems': totalitems})


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            temp = (p.quantity * p.product.discount_price)
            amount += temp
            total_amount = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount

        }
    return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            temp = (p.quantity * p.product.discount_price)
            amount += temp
            total_amount = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount

        }
    return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            temp = (p.quantity * p.product.discount_price)
            amount += temp
            total_amount = amount + shipping_amount
        data = {
            'amount': amount,
            'total_amount': total_amount

        }
    return JsonResponse(data)


@login_required
def buy_now(request):
    return render(request, 'buynow.html')


@login_required
def address(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'add': add, 'totalitems': totalitems})


@login_required
def orders(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', {'order_placed': op, 'totalitems': totalitems})


def mobile(request, data=None):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung' or data == 'Apple' or data == 'OnePlus' or data == 'Vivo':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(discount_price__lt=10001)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discount_price__gt=10000)
    return render(request, 'mobile.html', {'mobiles': mobiles, 'totalitems': totalitems})


def laptop(request, data=None):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Asus' or data == 'Apple' or data == 'HP' or data == 'Dell' or data == 'Acer':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(
            category='L').filter(discount_price__lt=50001)
    elif data == 'above':
        laptops = Product.objects.filter(
            category='L').filter(discount_price__gt=50000)
    return render(request, 'laptop.html', {'laptops': laptops, 'totalitems': totalitems})


def topwear(request, data=None):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'T-shirt' or data == 'Top' or data == 'Shirt' or data == 'Jacket':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(
            category='TW').filter(discount_price__lt=1001)
    elif data == 'above':
        topwears = Product.objects.filter(
            category='TW').filter(discount_price__gt=1000)
    return render(request, 'topwear.html', {'topwears': topwears, 'totalitems': totalitems})


def bottemwear(request, data=None):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        bottemwears = Product.objects.filter(category='BW')
    elif data == 'Jeans' or data == 'Pent' or data == 'Trouser' or data == 'Short':
        bottemwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottemwears = Product.objects.filter(
            category='BW').filter(discount_price__lt=1001)
    elif data == 'above':
        bottemwears = Product.objects.filter(
            category='BW').filter(discount_price__gt=1000)
    return render(request, 'bottemwear.html', {'bottemwears': bottemwears, 'totalitems': totalitems})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistraionForm()
        return render(request, 'customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistraionForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations !! Registered Successfully')
            form.save()
        return render(request, 'customerregistration.html', {'form': form})


@login_required
def checkout(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            temp = (p.quantity * p.product.discount_price)
            amount += temp
        total_amount = amount + shipping_amount
    return render(request, 'checkout.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items, 'totalitems': totalitems})


@login_required
def payment_done(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        totalitems = 0
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'profile.html', {'form': form, 'totalitems': totalitems})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            messages.success(
                request, 'Congratulations !! Profile Updated Successfully')
            reg.save()
        return redirect('address')
