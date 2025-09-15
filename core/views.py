from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm, ParqueaderoPrivadoForm, ProfileUpdateForm, UserUpdateForm, ValoracionForm
from .models import Profile, ParqueaderoPrivado, Valoracion, Reserva
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
import json
from django.core.mail import send_mail
from django.conf import settings
import datetime

def landing_page(request):
    return render(request, 'core/landing_page.html')

def reservarespacio(request):
    return render(request, 'core/reservarespacio.html')

def contactanos(request):
    return render(request, 'core/contactanos.html')

def contactanos_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        ciudad = request.POST.get('ciudad')
        mensaje = request.POST.get('mensaje')
        cuerpo = f"""
        Nombre: {nombre}
        Correo: {correo}
        Teléfono: {telefono}
        Ciudad: {ciudad}
        Mensaje: {mensaje}
        """
        send_mail(
            subject=f'Nuevo mensaje de contacto de {nombre}',
            message=cuerpo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        messages.success(request, '¡Tu mensaje ha sido enviado exitosamente!')
        return redirect('contactanos')
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
                        if profile.rol == 'admin':
                            return redirect('/dashboard/')
                        elif profile.rol == 'cliente':
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
            # Enviar correo de bienvenida
            send_mail(
                subject='¡Bienvenido a VIANApp!',
                message=f'Hola {form.cleaned_data["nombres"]},\n\n¡Gracias por registrarte en VIANApp! Ya puedes disfrutar de todos nuestros servicios.\n\nSaludos,\nEl equipo VIANApp',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data['email']],
                fail_silently=True,
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

def register_parqueadero(request):
    if request.method == 'POST':
        form = ParqueaderoPrivadoForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            nombre_dueno = form.cleaned_data['nombre_dueno']
            # Verificar si el usuario ya existe
            if User.objects.filter(username=email).exists():
                form.add_error('email', 'Ya existe un usuario con este correo electrónico.')
            else:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=nombre_dueno)
                # Eliminar perfil creado automáticamente por la señal si existe
                Profile.objects.filter(user=user).delete()
                # Crear perfil con rol parqueadero
                profile = Profile.objects.create(
                    user=user,
                    rol='parqueadero',
                    nombres=nombre_dueno,
                    telefono=form.cleaned_data['telefono'],
                    cedula=form.cleaned_data['documento_numero']
                )
                parqueadero = form.save(commit=False)
                parqueadero.email = email
                parqueadero.save()
                # Asociar automáticamente el parqueadero al perfil
                profile.parqueaderoprivado = parqueadero
                profile.save()
                # Enviar correo de bienvenida
                send_mail(
                    subject='¡Bienvenido a VIANApp!',
                    message=f'Hola {nombre_dueno},\n\n¡Gracias por registrar tu parqueadero en VIANApp! Ya puedes gestionar tus espacios y recibir clientes.\n\nSaludos,\nEl equipo VIANApp',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
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
    # Usar latitud y longitud directamente
    lat = float(parqueadero.latitud) if parqueadero.latitud is not None else 4.7110
    lng = float(parqueadero.longitud) if parqueadero.longitud is not None else -74.0721
    parqueadero.latitud = lat
    parqueadero.longitud = lng

    # Cancelar reserva si corresponde
    if request.method == 'POST' and 'cancelar_reserva_id' in request.POST:
        reserva_id = request.POST.get('cancelar_reserva_id')
        reserva = Reserva.objects.filter(id=reserva_id, parqueadero=parqueadero).first()
        if reserva:
            reserva.delete()
            messages.success(request, 'Reserva cancelada correctamente.')
        return redirect('mapa_parqueadero', pk=parqueadero.pk)

    if request.method == 'POST':
        # Guardar cambios de info general
        parqueadero.email = request.POST.get('email', parqueadero.email)
        parqueadero.direccion = request.POST.get('direccion', parqueadero.direccion)
        parqueadero.nombre_comercial = request.POST.get('nombre_comercial', parqueadero.nombre_comercial)
        parqueadero.telefono = request.POST.get('telefono', parqueadero.telefono)
        # Guardar tarifas y cupos
        if 'tarifa_hora' in request.POST:
            try:
                parqueadero.tarifa_hora = int(request.POST.get('tarifa_hora', parqueadero.tarifa_hora))
            except (ValueError, TypeError):
                pass
        if 'tarifa_dia' in request.POST:
            try:
                parqueadero.tarifa_dia = int(request.POST.get('tarifa_dia', parqueadero.tarifa_dia))
            except (ValueError, TypeError):
                pass
        if 'espacios' in request.POST:
            try:
                parqueadero.espacios = int(request.POST.get('espacios', parqueadero.espacios))
            except (ValueError, TypeError):
                pass
        if request.FILES.get('foto_parqueadero'):
            parqueadero.foto_parqueadero = request.FILES['foto_parqueadero']
        if request.FILES.get('foto_dueno'):
            parqueadero.foto_dueno = request.FILES['foto_dueno']
        parqueadero.save()
        return redirect('mapa_parqueadero', pk=parqueadero.pk)

    # Obtener reservas asociadas a este parqueadero
    reservas_parqueadero = Reserva.objects.filter(parqueadero=parqueadero).order_by('-fecha_hora')

    return render(request, 'core/maparqueadero.html', {
        'parqueadero': parqueadero,
        'reservas_parqueadero': reservas_parqueadero,
    })

@login_required
def mapcliente_view(request):
    if not hasattr(request.user, 'profile') or request.user.profile.rol != 'cliente':
        messages.error(request, 'Inicia sesión como cliente para acceder a esta vista.')
        return redirect('landing_page')

    # Cancelar reserva si corresponde
    if request.method == 'POST' and 'cancelar_reserva_id' in request.POST:
        reserva_id = request.POST.get('cancelar_reserva_id')
        reserva = Reserva.objects.filter(id=reserva_id, cedula=request.user.profile.cedula).first()
        if reserva:
            reserva.delete()
            messages.success(request, 'Reserva cancelada correctamente.')
        return redirect('mapcliente')

    parqueaderos = ParqueaderoPrivado.objects.all()
    parqueaderos_list = []
    for p in parqueaderos:
        if p.latitud and p.longitud:
            parqueaderos_list.append({
                "id": p.id,
                "nombre_comercial": p.nombre_comercial,
                "direccion": p.direccion,
                "ciudad": getattr(p, "ciudad", ""),
                "latitud": float(p.latitud),
                "longitud": float(p.longitud),
                "telefono": p.telefono,
                "tarifa_hora": str(getattr(p, "tarifa_hora", "")),
                "tarifa_dia": str(getattr(p, "tarifa_dia", "")),
                "espacios": p.espacios,
                "foto_parqueadero": p.foto_parqueadero.url if p.foto_parqueadero else "/static/core/img/imgparking1.jpg",
            })

    # Reservas activas del cliente (por cédula)
    reservas_cliente = Reserva.objects.filter(cedula=request.user.profile.cedula).order_by('-fecha_hora')

    # 🔎 Debug en terminal
    print("📌 Parqueaderos enviados al template:", parqueaderos_list)

    return render(request, "core/mapcliente.html", {
        "parqueaderos_json": json.dumps(parqueaderos_list),
        "reservas_cliente": reservas_cliente,
    }) 

@login_required
def reservarcliente_view(request, pk):
    # Solo clientes pueden acceder
    if not hasattr(request.user, 'profile') or request.user.profile.rol != 'cliente':
        messages.error(request, 'Inicia sesión como cliente para reservar un cupo.')
        return redirect('landing_page')
    parqueadero = get_object_or_404(ParqueaderoPrivado, pk=pk)
    user = request.user
    valoraciones_usuario = Valoracion.objects.filter(usuario=user, parqueadero=parqueadero)
    valoraciones_parqueadero = Valoracion.objects.filter(parqueadero=parqueadero).select_related('usuario').order_by('-fecha')
    puede_valorar = valoraciones_usuario.count() < 2
    form = ValoracionForm()

    # Guardar reserva si es POST y no es valoración
    if request.method == 'POST' and 'enviar_valoracion' not in request.POST:
        nombre = request.POST.get('nombre')
        # cedula = request.POST.get('cedula')  # No usar la del form
        telefono = request.POST.get('telefono')
        placa = request.POST.get('placa')
        tipo_vehiculo = request.POST.get('tipo_vehiculo')
        fecha_hora = request.POST.get('fecha_hora')
        cedula = user.profile.cedula  # Usar siempre la del perfil
        if nombre and cedula and telefono and placa and tipo_vehiculo and fecha_hora:
            # Convertir fecha_hora de string a datetime
            try:
                fecha_dt = datetime.datetime.strptime(fecha_hora, '%Y-%m-%dT%H:%M')
            except Exception:
                fecha_dt = None
            if fecha_dt:
                reserva = Reserva(
                    parqueadero=parqueadero,
                    nombre=nombre,
                    cedula=cedula,
                    telefono=telefono,
                    placa=placa,
                    tipo_vehiculo=tipo_vehiculo,
                    fecha_hora=fecha_dt
                )
                reserva.save()
                messages.success(request, '¡Reserva realizada exitosamente!')
                return redirect('reservarcliente', pk=pk)

    if request.method == 'POST' and 'enviar_valoracion' in request.POST:
        form = ValoracionForm(request.POST)
        if form.is_valid() and puede_valorar:
            nueva_valoracion = form.save(commit=False)
            nueva_valoracion.usuario = user
            nueva_valoracion.parqueadero = parqueadero
            count = Valoracion.objects.filter(usuario=user, parqueadero=parqueadero).count()
            if count >= 2:
                messages.error(request, 'Ya has dejado el máximo de 2 valoraciones para este parqueadero.')
            else:
                nueva_valoracion.save()
                messages.success(request, '¡Gracias por tu valoración!')
                return redirect('reservarcliente', pk=pk)
        elif not puede_valorar:
            messages.error(request, 'Ya has dejado el máximo de 2 valoraciones para este parqueadero.')
    return render(request, 'core/reservarcliente.html', {
        'parqueadero': parqueadero,
        'form_valoracion': form,
        'valoraciones_usuario': valoraciones_usuario,
        'valoraciones_parqueadero': valoraciones_parqueadero,
        'puede_valorar': puede_valorar,
    })

@login_required
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        # Si el usuario no tiene perfil, lo creamos con valores por defecto
        profile = Profile.objects.create(user=user, nombres=user.first_name or '', apellidos=user.last_name or '', telefono='', cedula='', departamento='', municipio='', placa='')
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)
    return render(request, 'core/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'user': user
    })
# Create your views here.
