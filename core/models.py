from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

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
    parqueaderoprivado = models.OneToOneField('ParqueaderoPrivado', on_delete=models.SET_NULL, null=True, blank=True, related_name='dueno_profile')

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

class ParqueaderoPrivado(models.Model):
    nombre_dueno = models.CharField(max_length=100)
    documento_tipo = models.CharField(max_length=20)
    documento_numero = models.CharField(max_length=30)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.CharField(max_length=200)
    nombre_comercial = models.CharField(max_length=100, blank=True, null=True)
    espacios = models.PositiveIntegerField()
    tipos_vehiculos = models.CharField(max_length=100)  # Coma separados
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    politicas = models.TextField(blank=True, null=True)
    foto_dueno = models.ImageField(upload_to='duenos_fotos/')
    foto_parqueadero = models.ImageField(upload_to='parqueaderos_fotos/')
    tarifa_hora = models.PositiveIntegerField(default=0)
    tarifa_dia = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.nombre_comercial or self.direccion} ({self.nombre_dueno})"

class Valoracion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    parqueadero = models.ForeignKey(ParqueaderoPrivado, on_delete=models.CASCADE)
    comentario = models.TextField(max_length=500)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'parqueadero', 'id')
        ordering = ['-fecha']

    def clean(self):
        # Limitar a 2 valoraciones por usuario y parqueadero
        if not self.usuario_id or not self.parqueadero_id:
            return  # No validar si aún no están asignados
        count = Valoracion.objects.filter(usuario=self.usuario, parqueadero=self.parqueadero).exclude(pk=self.pk).count()
        if count >= 2:
            raise ValidationError('Solo puedes dejar hasta 2 valoraciones para este parqueadero.')

    def save(self, *args, **kwargs):
        # Solo llamar a full_clean si usuario y parqueadero ya están asignados
        if self.usuario_id and self.parqueadero_id:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username} - {self.parqueadero} - {self.rating} estrellas"

class Reserva(models.Model):
    parqueadero = models.ForeignKey(ParqueaderoPrivado, on_delete=models.CASCADE, related_name='reservas')
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    placa = models.CharField(max_length=20)
    tipo_vehiculo = models.CharField(max_length=20)
    fecha_hora = models.DateTimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.parqueadero.nombre_comercial} - {self.fecha_hora}"

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # Si es superuser, el perfil será admin
        rol = 'admin' if instance.is_superuser else 'cliente'
        Profile.objects.create(user=instance, rol=rol, nombres=instance.first_name or '', apellidos=instance.last_name or '', telefono='', cedula='', departamento='', municipio='', placa='')
    else:
        # Si el usuario ya existe y es superuser, aseguramos que el perfil sea admin
        try:
            profile = instance.profile
            if instance.is_superuser and profile.rol != 'admin':
                profile.rol = 'admin'
                profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance, rol='admin' if instance.is_superuser else 'cliente', nombres=instance.first_name or '', apellidos=instance.last_name or '', telefono='', cedula='', departamento='', municipio='', placa='')
