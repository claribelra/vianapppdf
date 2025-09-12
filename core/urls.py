from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from . import views
from .views import register, login_view, profile_view
from .views_password import password_reset_request
from .views_password_reset import password_reset_confirm

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
    path('mapcliente/', views.mapcliente_view, name='mapcliente'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('registro-parqueadero/', views.register_parqueadero, name='register_parqueadero'),
    path('mapa-parqueadero/<int:pk>/', views.mapa_parqueadero, name='mapa_parqueadero'),
    path('reservarcliente/<int:pk>/', views.reservarcliente_view, name='reservarcliente'),
    path('recuperar/', password_reset_request, name='password_reset_request'),
    path('reset-password/<int:user_id>/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
]
