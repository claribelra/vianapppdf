from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from . import views
from .views import register, login_view

def mapcliente_view(request):
    return render(request, 'core/mapcliente.html')

@login_required
def profile(request):
    return render(request, 'core/profile.html', {'user': request.user, 'profile': request.user.profile})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('reservarespacio/', views.reservarespacio, name='reservarespacio'),
    path('contactanos/', views.contactanos, name='contactanos'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('servicios/', views.servicios, name='servicios'),
    path('mapcliente/', mapcliente_view, name='mapcliente'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
]
