from django.urls import path
from .views import admin_dashboard, usuarios_list, toggle_usuario, parqueaderos_list, comentarios_list, comentarios_parqueadero, eliminar_comentario

urlpatterns = [
    path('', admin_dashboard, name='dashboard_admin'),
    path('usuarios/', usuarios_list, name='dashboard_usuarios'),
    path('usuarios/toggle/<int:user_id>/', toggle_usuario, name='dashboard_toggle_usuario'),
    path('parqueaderos/', parqueaderos_list, name='dashboard_parqueaderos'),
    path('comentarios/', comentarios_list, name='dashboard_comentarios'),
    path('comentarios/<int:pk>/', comentarios_parqueadero, name='dashboard_comentarios_parqueadero'),
    path('comentarios/<int:pk>/eliminar/<int:valoracion_id>/', eliminar_comentario, name='dashboard_eliminar_comentario'),
]
