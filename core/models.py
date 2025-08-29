from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    ROLES = (
        ('admin', 'Admin'),
        ('cliente', 'Cliente'),
        ('parqueadero', 'Parqueadero'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    genero = models.CharField(max_length=20, blank=True)
    cedula = models.CharField(max_length=30)
    departamento = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    placa = models.CharField(max_length=20)
    tarjeta = models.ImageField(upload_to='tarjetas/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
