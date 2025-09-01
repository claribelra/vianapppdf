from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm, ParqueaderoPrivadoForm
from .models import Profile, ParqueaderoPrivado
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
import json

def landing_page(request):
    return render(request, 'core/landing_page.html')

def reservarespacio(request):
    return render(request, 'core/reservarespacio.html')

def contactanos(request):
    return render(request, 'core/contactanos.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Buscar usuario por username o email
            user = User.objects.filter(username=username_or_email).first()
            if not user:
                user = User.objects.filter(email=username_or_email).first()
            if user:
                user_auth = authenticate(request, username=user.username, password=password)
                if user_auth is not None:
                    auth_login(request, user_auth)
                    try:
                        profile = user_auth.profile
                        if profile.rol == 'cliente':
                            return redirect('mapcliente')
                        elif profile.rol == 'parqueadero':
                            parqueadero = ParqueaderoPrivado.objects.filter(email=user_auth.email).first()
                            if parqueadero:
                                return redirect('mapa_parqueadero', pk=parqueadero.pk)
                            else:
                                return redirect('landing_page')
                    except Profile.DoesNotExist:
                        pass
                    return redirect('landing_page')
                else:
                    form.add_error(None, 'Usuario o contraseña incorrectos')
            else:
                form.add_error('username', 'Usuario o correo no encontrado')
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(
                user=user,
                rol=form.cleaned_data['rol'],
                nombres=form.cleaned_data['nombres'],
                apellidos=form.cleaned_data['apellidos'],
                telefono=form.cleaned_data['telefono'],
                genero=form.cleaned_data.get('genero', ''),
                cedula=form.cleaned_data['cedula'],
                departamento=form.cleaned_data['departamento'],
                municipio=form.cleaned_data['municipio'],
                placa=form.cleaned_data['placa'],
                tarjeta=form.cleaned_data.get('tarjeta', None)
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

def register_parqueadero(request):
    if request.method == 'POST':
        form = ParqueaderoPrivadoForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear usuario para el parqueadero
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            nombre_dueno = form.cleaned_data['nombre_dueno']
            # Usar email como username
            user = User.objects.create_user(username=email, email=email, password=password, first_name=nombre_dueno)
            # Crear perfil con rol parqueadero
            Profile.objects.create(
                user=user,
                rol='parqueadero',
                nombres=nombre_dueno,
                telefono=form.cleaned_data['telefono'],
                cedula=form.cleaned_data['documento_numero']
            )
            # Guardar datos del parqueadero
            parqueadero = form.save(commit=False)
            parqueadero.email = email
            parqueadero.save()
            return redirect('login')
    else:
        form = ParqueaderoPrivadoForm()
    return render(request, 'core/register_parqueadero.html', {'form': form})

def servicios(request):
    return render(request, 'core/servicios.html')

@login_required
def mapa_parqueadero(request, pk):
    if not hasattr(request.user, 'profile') or request.user.profile.rol != 'parqueadero':
        messages.error(request, 'Inicia sesión como parqueadero para acceder a esta vista.')
        return redirect('landing_page')
    parqueadero = get_object_or_404(ParqueaderoPrivado, pk=pk)
    # Procesar ubicacion_mapa para obtener lat/lng
    lat, lng = 4.7110, -74.0721  # Default Bogotá
    ubicacion = parqueadero.ubicacion_mapa.strip() if parqueadero.ubicacion_mapa else ''
    if ubicacion:
        try:
            partes = ubicacion.split(',')
            if len(partes) == 2:
                lat = float(partes[0])
                lng = float(partes[1])
        except Exception:
            pass
    parqueadero.latitud = lat
    parqueadero.longitud = lng

    if request.method == 'POST':
        parqueadero.email = request.POST.get('email', parqueadero.email)
        parqueadero.direccion = request.POST.get('direccion', parqueadero.direccion)
        parqueadero.nombre_comercial = request.POST.get('nombre_comercial', parqueadero.nombre_comercial)
        parqueadero.telefono = request.POST.get('telefono', parqueadero.telefono)
        if request.FILES.get('foto_parqueadero'):
            parqueadero.foto_parqueadero = request.FILES['foto_parqueadero']
        if request.FILES.get('foto_dueno'):
            parqueadero.foto_dueno = request.FILES['foto_dueno']
        parqueadero.save()
        return redirect('mapa_parqueadero', pk=parqueadero.pk)

    return render(request, 'core/maparqueadero.html', {'parqueadero': parqueadero})

@login_required
def mapcliente_view(request):
    if not hasattr(request.user, 'profile') or request.user.profile.rol != 'cliente':
        messages.error(request, 'Inicia sesión como cliente para acceder a esta vista.')
        return redirect('landing_page')
    parqueaderos = ParqueaderoPrivado.objects.all()
    parqueaderos_list = [
        {
            'id': p.id,
            'latitud': float(p.ubicacion_mapa.split(',')[0]) if p.ubicacion_mapa and ',' in p.ubicacion_mapa else None,
            'longitud': float(p.ubicacion_mapa.split(',')[1]) if p.ubicacion_mapa and ',' in p.ubicacion_mapa else None,
            'ciudad': getattr(p, 'ciudad', ''),
            'nombre_comercial': p.nombre_comercial,
            'direccion': p.direccion,
            'tarifa_hora': getattr(p, 'tarifa_hora', ''),
            'espacios': p.espacios,
            'telefono': p.telefono,
            'foto_parqueadero': p.foto_parqueadero.url if p.foto_parqueadero else '/static/core/img/imgparking1.jpg',
        } for p in parqueaderos if p.ubicacion_mapa and ',' in p.ubicacion_mapa
    ]
    parqueaderos_json = json.dumps(parqueaderos_list)
    return render(request, 'core/mapcliente.html', {'parqueaderos_json': parqueaderos_json, 'parqueaderos_list': parqueaderos_list})

@login_required
def reservarcliente_view(request, pk):
    # Solo clientes pueden acceder
    if not hasattr(request.user, 'profile') or request.user.profile.rol != 'cliente':
        messages.error(request, 'Inicia sesión como cliente para reservar un cupo.')
        return redirect('landing_page')
    parqueadero = get_object_or_404(ParqueaderoPrivado, pk=pk)
    return render(request, 'core/reservarcliente.html', {'parqueadero': parqueadero})
# Create your views here.
