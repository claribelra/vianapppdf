from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from core.models import ParqueaderoPrivado, Valoracion

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.rol == 'admin')

@user_passes_test(is_admin)
@login_required
def admin_dashboard(request):
    return render(request, 'dashboard_admin/dashboard.html', {'section': 'inicio'})

@user_passes_test(is_admin)
@login_required
def usuarios_list(request):
    usuarios = User.objects.select_related('profile').all().order_by('-is_active', 'profile__rol', 'profile__nombres')
    return render(request, 'dashboard_admin/dashboard.html', {
        'section': 'usuarios',
        'usuarios': usuarios
    })

@user_passes_test(is_admin)
@login_required
def parqueaderos_list(request):
    parqueaderos = list(ParqueaderoPrivado.objects.all().order_by('nombre_comercial'))
    usuarios = list(User.objects.all())
    return render(request, 'dashboard_admin/dashboard.html', {
        'section': 'parqueaderos',
        'parqueaderos': parqueaderos,
        'usuarios': usuarios,
    })

@user_passes_test(is_admin)
@login_required
def comentarios_list(request):
    parqueaderos = ParqueaderoPrivado.objects.all().order_by('nombre_comercial')
    return render(request, 'dashboard_admin/dashboard.html', {
        'section': 'comentarios',
        'parqueaderos': parqueaderos,
    })

@user_passes_test(is_admin)
@login_required
def comentarios_parqueadero(request, pk):
    parqueadero = get_object_or_404(ParqueaderoPrivado, pk=pk)
    valoraciones = Valoracion.objects.filter(parqueadero=parqueadero).select_related('usuario').order_by('-fecha')
    return render(request, 'dashboard_admin/dashboard.html', {
        'section': 'ver_comentarios',
        'parqueadero': parqueadero,
        'valoraciones': valoraciones,
    })

@user_passes_test(is_admin)
@csrf_exempt
@login_required
def eliminar_comentario(request, pk, valoracion_id):
    parqueadero = get_object_or_404(ParqueaderoPrivado, pk=pk)
    valoracion = get_object_or_404(Valoracion, pk=valoracion_id, parqueadero=parqueadero)
    if request.method == 'POST':
        valoracion.delete()
        messages.success(request, 'Comentario eliminado correctamente.')
        return redirect(f'/dashboard/comentarios/{pk}/')
    return redirect(f'/dashboard/comentarios/{pk}/')

@user_passes_test(is_admin)
@csrf_protect
@login_required
def toggle_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f'El usuario {user.username} ha sido actualizado.')
    return redirect('dashboard_usuarios')

# Create your views here.
