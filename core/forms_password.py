from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo registrado',
            'style': 'border-radius:10px;max-width:340px;width:100%;margin:auto;'
        })
    )
