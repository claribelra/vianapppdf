from django import forms
from django.contrib.auth.models import User
from .models import Profile

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
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
