from django.shortcuts import render, redirect

def BASE(request):
    return render(request, 'Main/base.html')

def HOME(request):
    return render(request, 'Main/index.html')

def login(request):
    return render(request, 'Main/login.html')