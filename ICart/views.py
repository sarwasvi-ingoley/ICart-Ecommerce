from django.shortcuts import render, redirect
from ICartApp.models import Product, SubCategory, FilterPrice, Color
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def BASE(request):
    return render(request, 'Main/base.html')

def HOME(request):
    product=Product.objects.filter(status='Publish', condition='New')
    context={
        'product':product,
    }

    return render(request, 'Main/index.html', context)

def PRODUCT(request):
    product=Product.objects.filter(status='Publish')
    subcategory=SubCategory.objects.all()
    filterprice=FilterPrice.objects.all()
    color=Color.objects.all()

    SUBCATID=request.GET.get('subcategory')
    PRICE_FILTER_ID=request.GET.get('filterprice')
    COLOR_ID=request.GET.get('color')

    ATOZID=request.GET.get('ATOZ')
    ZTOAID=request.GET.get('ZTOA')
    PRICE_LOW_TO_HIGH_ID=request.GET.get('PRICE_LOW_TO_HIGH')
    PRICE_HIGH_TO_LOW_ID=request.GET.get('PRICE_HIGH_TO_LOW')
    NEW_ID=request.GET.get('NEW')
    OLD_ID=request.GET.get('OLD')

    if SUBCATID:
        product=Product.objects.filter(subcategory=SUBCATID, status='Publish')
    elif PRICE_FILTER_ID:
        product=Product.objects.filter(filter_price=PRICE_FILTER_ID, status='Publish')
    elif COLOR_ID:
        product=Product.objects.filter(color=COLOR_ID, status='Publish')
    elif ATOZID:
        product=Product.objects.filter(status='Publish').order_by('name')
    elif ZTOAID:
        product=Product.objects.filter(status='Publish').order_by('-name')
    elif PRICE_LOW_TO_HIGH_ID:
        product=Product.objects.filter(status='Publish').order_by('price')
    elif PRICE_HIGH_TO_LOW_ID:
        product=Product.objects.filter(status='Publish').order_by('-price')
    elif NEW_ID:
        product=Product.objects.filter(status='Publish', condition='New').order_by('-id')
    elif OLD_ID:
        product=Product.objects.filter(status='Publish', condition='Old').order_by('-id')
    else:
        product=Product.objects.filter(status='Publish').order_by('-id')

    context={
        'product':product,
        'subcategory': subcategory,
        'filterprice': filterprice,
        'color':color,
    }
    return render(request, 'Main/product.html',context)


def SEARCH(request):
    query=request.GET.get('query')
    if query:
        product=Product.objects.filter(name__icontains=query)
    else:
        product=None
    context={
        'product':product,
    }
    return render(request, 'Main/search.html',context)


def PRODUCT_DETAIL_PAGE(request, id):
    prod=Product.objects.filter(id=id).first()
    context={
        'prod':prod
    }
    return render(request, 'Main/product_single.html', context)


def Handleregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        Firstname = request.POST.get('Firstname')
        Lastname = request.POST.get('Lastname')
        Email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        customer = User.objects.create_user(username=username, email=Email, password=password1)
        customer.first_name = Firstname
        customer.last_name = Lastname
        customer.save()

        return redirect('register')


    return render(request, 'Main/Registration/auth.html')

def Handlelogin(request):
    if request.method == 'POST':
        username = request.POST.get('username1')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
        
    return render(request, 'Main/Registration/auth.html')

def Handlelogout(request):
    logout(request)
    return redirect('home')