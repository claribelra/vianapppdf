from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm
from .models import Profile

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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Redirección según rol
                try:
                    profile = user.profile
                    if profile.rol == 'cliente':
                        return redirect('mapcliente')
                except Profile.DoesNotExist:
                    pass
                return redirect('landing_page')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
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

def servicios(request):
    return render(request, 'core/servicios.html')

# Create your views here.
