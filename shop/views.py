from django.shortcuts import render, redirect
from shop.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
def home(request):
    products = Products.objects.filter(trending=1)
    return render(request, "shop/index.html", {"products": products})
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out Successfully")
    return redirect('/')

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect("/login")
    return render(request, "shop/login.html")

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success..You Can Login Now..!")
            return redirect('/login')
    return render(request, "shop/register.html", {'form': form})

def collections(request):
    category = Category.objects.filter(status=0)
    return render(request, "shop/collections.html", {"Category": category})

def collectionsview(request, name):
    try:
        category = Category.objects.get(name=name, status=0)
        products = Products.objects.filter(category=category)
        return render(request, "shop/products/index.html", {"products": products, "category_name": name})
    except Category.DoesNotExist:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')

def product_details(request, cname, pname):
    if Category.objects.filter(name=cname, status=0):
        if Products.objects.filter(name=pname, status=0):
            products = Products.objects.filter(name=pname, status=0).first()
            return render(request, "shop/products/product_details.html", {"products": products})
        else:
            messages.error(request, "No Such Product Found")
            return redirect('collections')
    else:
        messages.error(request, "No Such Category Found")
        return redirect('collections')

def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']

            try:
                product = Products.objects.get(id=product_id)
                if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                    return JsonResponse({'status': 'Product Already in the Cart'}, status=200)
                else:
                    if product.quantity >= product_qty:
                        Cart.objects.create(
                            user=request.user,
                            product=product,
                            product_qty=product_qty
                        )
                        return JsonResponse({'status': 'Product Added to Cart Successfully'}, status=200)
                    else:
                        return JsonResponse({'status': 'Not Enough Quantity Available'}, status=200)
            except Products.DoesNotExist:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
        else:
            return JsonResponse({'status': 'Login to Add to Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect("/")
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Products.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)