from django.shortcuts import render, redirect
from ICartApp.models import Product, SubCategory, FilterPrice, Color, ImageUpload
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cart.cart import Cart
import numpy as np
from PIL import Image
from .feature_extractor import FeatureExtractor
from datetime import datetime
from pathlib import Path
import os


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

def upload_file(request):
    response=[]
    if request.method == 'POST':
        # get the data from the ajax post request
        print(request)

    # print(request.FILES.getlist('file'))
    # print(request.FILES['file'])  # for single file
    print('file: ', request.FILES)
    doc=ImageUpload.objects.create(user_image=request.FILES['file'])
    print('doc: ', doc.user_image)
    request.session['uploadImage'] = str(doc.user_image)
    print(request.session['uploadImage'])
    response.append(doc.user_image.url)
    return JsonResponse(response, safe=False)

#def search_image2(request):
#    imgsrc = ''
#    if request.session.has_key('uploadImage'):
#        if(request.session['uploadImage']):
#            imgsrc = request.session['uploadImage']
#    print(imgsrc)
#    request.session['uploadImage'] = ''
#    context = {
#        'imgsrc': imgsrc,
#    }
#    return render(request,'Main/search_image.html', context)

def search_image(request):
    fe = FeatureExtractor()
    features = []
    img_paths = []
    for feature_path in Path("static/feature").glob("*.npy"):
        features.append(np.load(feature_path))
        img_paths.append(Path("static/img") / (feature_path.stem + ".jpg"))
    features = np.array(features)
    

    imgsrc = ''
    if 'uploadImage' in request.session:
        if request.session['uploadImage']:
            imgsrc = request.session['uploadImage']
            img = Image.open(imgsrc)
            query = fe.extract(img)
            dists = np.linalg.norm(features-query, axis=1)
            ids = np.argsort(dists)[:30] 
            scores = [(dists[id], img_paths[id]) for id in ids]
            context = {'query_path': imgsrc, 'scores': scores}
            print(imgsrc)
    #file_path = request.session['uploadImage']
    #with open(file_path, 'rb') as f:
    #    img = Image.open(f)
    #uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + os.path.basename(file_path)
    ##img.save(uploaded_img_path)
    #query = fe.extract(img)
    #dists = np.linalg.norm(features-query, axis=1)  
#
    
    return render(request,'Main/search_image.html',context)
   
    #imgsrc = ''
    #if 'uploadImage' in request.session:
    #    if request.session['uploadImage']:
    #        imgsrc = request.session['uploadImage']
    #print(imgsrc)
    #file = imgsrc
    #
    #img = Image.open(file)
    #
    #uploaded_img_path = "static/uploaded" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
    #img.save(uploaded_img_path)

    #query = fe.extract(img)
    #dists = np.linalg.norm(features-query, axis=1)  
    #
    #ids = np.argsort(dists)[:30] 
    #scores = [(dists[id], str(img_paths[id])) for id in ids]
    #
    #context = {'query_path': uploaded_img_path, 'scores': scores}
    #print("11")
    #return render(request, 'Main/search_image.html', context)
    

#def search_image1(request):
#    fe = FeatureExtractor()
#    features = []
#    img_paths = []
#    for feature_path in Path("./static/feature").glob("*.npy"):
#        features.append(np.load(feature_path))
#        img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
#    features = np.array(features)
#    if request.method == 'POST':
#        imgsrc = ''
#        if request.session.has_key('uploadImage'):
#            if(request.session['uploadImage']):
#                imgsrc = request.session['uploadImage']
#        print(imgsrc)
#        file = request.session['uploadImage']
#
#        
#        img = Image.open(file.stream)  
#        uploaded_img_path = "static/image" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
#        img.save(uploaded_img_path)
#
#       
#        query = fe.extract(img)
#        dists = np.linalg.norm(features-query, axis=1)  
#        ids = np.argsort(dists)[:30] 
#        scores = [(dists[id], img_paths[id]) for id in ids]
#        query_path=uploaded_img_path
#        context = {
#        'imgsrc': query_path,
#    }
#        return render(request,'Main/search_image.html',context)
#        
#    else:
#        return render(request,'Main/search_image.html')
#

@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'Main/Cart/cart_details.html')


def checkout(request):
    return render(request, 'Main/Cart/checkout.html')

