from django.shortcuts import render

def landing_page(request):
    return render(request, 'core/landing_page.html')

def reservarespacio(request):
    return render(request, 'core/reservarespacio.html')

def contactanos(request):
    return render(request, 'core/contactanos.html')

def login(request):
    return render(request, 'core/login.html')

def register(request):
    return render(request, 'core/register.html')

def servicios(request):
    return render(request, 'core/servicios.html')

# Create your views here.
