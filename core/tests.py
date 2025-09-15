from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Profile, ParqueaderoPrivado

# Eliminar todos los usuarios y perfiles
Profile.objects.all().delete()
User.objects.all().delete()
ParqueaderoPrivado.objects.all().delete()

# Crear admin
admin_user = User.objects.create_superuser('admin', 'admin@vianapp.com', 'admin1234')
admin_profile = Profile.objects.get(user=admin_user)
admin_profile.rol = 'admin'
admin_profile.save()

# Crear cliente
cliente_user = User.objects.create_user('cliente', 'cliente@vianapp.com', 'cliente1234', first_name='Cliente')
cliente_profile = Profile.objects.get(user=cliente_user)
cliente_profile.rol = 'cliente'
cliente_profile.nombres = 'Cliente'
cliente_profile.save()

# Crear parqueadero
parqueadero_user = User.objects.create_user('parqueadero', 'parqueadero@vianapp.com', 'parqueadero1234', first_name='Parqueadero')
parqueadero_profile = Profile.objects.get(user=parqueadero_user)
parqueadero_profile.rol = 'parqueadero'
parqueadero_profile.nombres = 'Parqueadero'
parqueadero_profile.save()
parqueadero = ParqueaderoPrivado.objects.create(
    nombre_dueno='Parqueadero',
    documento_tipo='CC',
    documento_numero='123456789',
    telefono='3101234567',
    email='parqueadero@vianapp.com',
    direccion='Calle 123 #45-67',
    nombre_comercial='Parqueadero Prueba',
    espacios=10,
    tipos_vehiculos='carros,motos',
    latitud=4.7110,
    longitud=-74.0721,
    tarifa_hora=5000,
    tarifa_dia=30000,
    foto_dueno='persona.jpeg',
    foto_parqueadero='parksanta.jpg'
)
parqueadero_profile.parqueaderoprivado = parqueadero
parqueadero_profile.save()
print('Usuarios y perfiles de prueba creados correctamente.')
