from django import forms
from django.contrib.auth.models import User
from .models import Profile, ParqueaderoPrivado

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    rol = forms.ChoiceField(choices=Profile.ROLES, label='Rol')
    nombres = forms.CharField(max_length=100, label='Nombres')
    apellidos = forms.CharField(max_length=100, label='Apellidos')
    telefono = forms.CharField(max_length=20, label='Teléfono')
    genero = forms.CharField(max_length=20, required=False, label='Género')
    cedula = forms.CharField(max_length=30, label='Cédula')
    departamento = forms.CharField(max_length=50, label='Departamento')
    municipio = forms.CharField(max_length=50, label='Municipio')
    placa = forms.CharField(max_length=20, label='Placa')
    tarjeta = forms.ImageField(required=False, label='Tarjeta de propiedad')
    username = forms.CharField(label='Usuario')
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Usuario o correo electrónico', widget=forms.TextInput(attrs={'placeholder': 'Usuario o correo electrónico'}))
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class ParqueaderoPrivadoForm(forms.ModelForm):
    DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de ciudadanía'),
        ('CE', 'Cédula de extranjería'),
        ('NIT', 'NIT'),
        ('PAS', 'Pasaporte'),
        ('Otro', 'Otro'),
    ]
    documento_tipo = forms.ChoiceField(choices=DOCUMENTO_CHOICES, required=True, label='Tipo de documento')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña', required=True)
    latitud = forms.DecimalField(label='Latitud', required=True, max_digits=9, decimal_places=6)
    longitud = forms.DecimalField(label='Longitud', required=True, max_digits=9, decimal_places=6)

    class Meta:
        model = ParqueaderoPrivado
        fields = [
            'nombre_dueno', 'documento_tipo', 'documento_numero', 'telefono', 'email',
            'direccion', 'nombre_comercial', 'espacios', 'tipos_vehiculos',
            'latitud', 'longitud', 'politicas', 'foto_dueno', 'foto_parqueadero', 'password'
        ]
        widgets = {
            'tipos_vehiculos': forms.TextInput(attrs={'placeholder': 'Ejemplo: carros, motos, bicicletas'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foto_dueno'].required = True
        self.fields['foto_parqueadero'].required = True
        self.fields['password'].required = True

class ProfileUpdateForm(forms.ModelForm):
    nombres = forms.CharField(max_length=100, label='Nombres')
    apellidos = forms.CharField(max_length=100, label='Apellidos')
    telefono = forms.CharField(max_length=20, label='Teléfono')
    genero = forms.CharField(max_length=20, required=False, label='Género')
    departamento = forms.CharField(max_length=50, label='Departamento')
    municipio = forms.CharField(max_length=50, label='Municipio')
    placa = forms.CharField(max_length=20, label='Placa')
    tarjeta = forms.ImageField(required=False, label='Tarjeta de propiedad')

    class Meta:
        model = Profile
        fields = ['nombres', 'apellidos', 'telefono', 'genero', 'departamento', 'municipio', 'placa', 'tarjeta']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Correo')
    class Meta:
        model = User
        fields = ['email']
