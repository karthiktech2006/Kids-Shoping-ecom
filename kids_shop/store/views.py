from itertools import product
from django.shortcuts import render,redirect, get_object_or_404 # type: ignore
from .models import Product
from django.contrib import messages

import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404


def home(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def search_view(request):
    query = request.GET.get('query', '')  # Make sure it's 'query' not 'q'
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'store/search.html', {'products': products, 'query': query})


from django.contrib.auth.decorators import login_required

@login_required
def cart_view(request):
    cart_ids = request.session.get('cart', [])
    products = Product.objects.filter(pk__in=cart_ids)
    return render(request, 'store/cart.html', {'products': products})

@login_required
def index(request):
    print("Logged in user:", request.user)
    return render(request, 'store/index.html', {'products': Product.objects.all()})

def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'buy_now.html', {'product': product})


def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    
    # Add the product to a cart model or session
    cart = request.session.get('cart', [])
    if pk not in cart:
        cart.append(pk)
        request.session['cart'] = cart
        messages.success(request, f"{product.name} added to cart!")

    return redirect('cart_view')


def remove_from_cart(request, pk):
    cart = request.session.get('cart', [])
    if pk in cart:
        cart.remove(pk)
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    return redirect('cart_view')
  

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(name__icontains=query)
    return render(request, 'store/search.html', {'products': results, 'query': query})


import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404


def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)
    amount = int(product.price * 100)  # Razorpay expects amount in paise

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 1})

    context = {
        'product': product,
        'amount': amount,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': payment['id'],
        'user': request.user,
    }
    return render(request, 'store/payment.html', context)


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SimpleUserCreationForm



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('index')
        
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            
    else:
        form = SimpleUserCreationForm()
    return render(request, 'store/register.html', {'form': form})