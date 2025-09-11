from django.urls import path
from .views import admin_dashboard, usuarios_list, toggle_usuario, parqueaderos_list

urlpatterns = [
    path('', admin_dashboard, name='dashboard_admin'),
    path('usuarios/', usuarios_list, name='dashboard_usuarios'),
    path('usuarios/toggle/<int:user_id>/', toggle_usuario, name='dashboard_toggle_usuario'),
    path('parqueaderos/', parqueaderos_list, name='dashboard_parqueaderos'),
]
