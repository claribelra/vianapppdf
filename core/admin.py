from django.contrib import admin
from .models import Profile, ParqueaderoPrivado

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'nombres', 'apellidos', 'parqueaderoprivado')
    search_fields = ('user__username', 'nombres', 'apellidos', 'rol')

class ParqueaderoPrivadoAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercial', 'direccion', 'nombre_dueno', 'telefono')
    search_fields = ('nombre_comercial', 'direccion', 'nombre_dueno')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ParqueaderoPrivado, ParqueaderoPrivadoAdmin)

# Register your models here.
