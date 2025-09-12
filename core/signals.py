from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        rol = 'admin' if instance.is_superuser else 'cliente'
        Profile.objects.get_or_create(
            user=instance,
            defaults={
                'rol': rol,
                'nombres': instance.first_name or '',
                'apellidos': instance.last_name or '',
                'telefono': '',
                'cedula': '',
                'departamento': '',
                'municipio': '',
                'placa': ''
            }
        )
    else:
        try:
            profile = instance.profile
            if instance.is_superuser and profile.rol != 'admin':
                profile.rol = 'admin'
                profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance, rol='admin' if instance.is_superuser else 'cliente', nombres=instance.first_name or '', apellidos=instance.last_name or '', telefono='', cedula='', departamento='', municipio='', placa='')
