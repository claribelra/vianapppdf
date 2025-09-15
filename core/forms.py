from django import forms
from django.contrib.auth.models import User
from .models import Profile, ParqueaderoPrivado, Valoracion

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
    latitud = forms.DecimalField(label='Latitud', required=True, max_digits=9, decimal_places=6, help_text='Ejemplo: 4.7110')
    longitud = forms.DecimalField(label='Longitud', required=True, max_digits=9, decimal_places=6, help_text='Ejemplo: -74.0721')

    class Meta:
        model = ParqueaderoPrivado
        fields = [
            'nombre_dueno', 'documento_tipo', 'documento_numero', 'telefono', 'email',
            'direccion', 'nombre_comercial', 'espacios', 'tipos_vehiculos',
            'latitud', 'longitud', 'politicas', 'foto_dueno', 'foto_parqueadero', 'password'
        ]
        widgets = {
            'tipos_vehiculos': forms.TextInput(attrs={'placeholder': 'Ejemplo: carros, motos, bicicletas'}),
            'politicas': forms.Textarea(attrs={'placeholder': 'Ejemplo: No se permite fumar. El parqueadero no se hace responsable por objetos dejados dentro del vehículo.', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foto_dueno'].required = True
        self.fields['foto_parqueadero'].required = True
        self.fields['password'].required = True
        self.fields['nombre_dueno'].help_text = 'Nombre completo del propietario del parqueadero.'
        self.fields['documento_numero'].help_text = 'Número de documento válido. Ejemplo: 1234567890.'
        self.fields['telefono'].help_text = 'Incluye el indicativo si es necesario. Ejemplo: 3101234567.'
        self.fields['email'].help_text = 'Correo electrónico válido. Se usará para acceder y recibir notificaciones.'
        self.fields['direccion'].help_text = 'Dirección exacta del parqueadero.'
        self.fields['nombre_comercial'].help_text = 'Nombre visible para los clientes (opcional).'
        self.fields['espacios'].help_text = 'Cantidad de cupos disponibles. Debe ser mayor a 0.'
        self.fields['tipos_vehiculos'].help_text = 'Ejemplo: carros, motos, bicicletas.'
        self.fields['politicas'].help_text = 'Reglas o condiciones del parqueadero (opcional).'
        self.fields['foto_dueno'].help_text = 'Foto clara del dueño para mayor confianza.'
        self.fields['foto_parqueadero'].help_text = 'Foto del parqueadero para mostrar a los clientes.'
        self.fields['password'].help_text = 'Mínimo 8 caracteres. Usa letras y números.'

    def clean_espacios(self):
        espacios = self.cleaned_data.get('espacios')
        if espacios is not None and espacios <= 0:
            raise forms.ValidationError('La cantidad de cupos debe ser mayor a 0.')
        return espacios

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and ParqueaderoPrivado.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un parqueadero registrado con este correo electrónico.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if password and password.isdigit():
            raise forms.ValidationError('La contraseña no puede ser solo números. Usa letras y números.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get('latitud')
        lng = cleaned_data.get('longitud')
        if lat is not None and (lat < -90 or lat > 90):
            self.add_error('latitud', 'La latitud debe estar entre -90 y 90.')
        if lng is not None and (lng < -180 or lng > 180):
            self.add_error('longitud', 'La longitud debe estar entre -180 y 180.')
        return cleaned_data

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

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['rating', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows':2, 'placeholder':'Escribe tu comentario...', 'class':'form-control', 'style':'border-radius:10px;'}),
            'rating': forms.Select(choices=[(i, f"{i} estrella{'s' if i > 1 else ''}") for i in range(1,6)], attrs={'class':'form-control', 'style':'border-radius:10px;'}),
        }
        labels = {
            'rating': 'Calificación',
            'comentario': 'Comentario',
        }
