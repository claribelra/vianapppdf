from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('reservarespacio/', views.reservarespacio, name='reservarespacio'),
    path('contactanos/', views.contactanos, name='contactanos'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('servicios/', views.servicios, name='servicios'),
]
