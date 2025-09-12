from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms_password import PasswordResetRequestForm

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                # Generar un token simple (en producción usa PasswordResetTokenGenerator)
                token = user.password[:10]  # Solo para demo, NO seguro
                reset_link = request.build_absolute_uri(f'/reset-password/{user.pk}/{token}/')
                send_mail(
                    subject='Recupera tu contraseña en VIANApp',
                    message=f'Hola,\n\nPara restablecer tu contraseña haz clic en el siguiente enlace:\n{reset_link}\n\nSi no solicitaste este correo, ignóralo.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
                messages.success(request, 'Te hemos enviado un correo con instrucciones para restablecer tu contraseña.')
                return redirect('login')
            else:
                messages.error(request, 'No existe una cuenta con ese correo.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'core/password_reset_request.html', {'form': form})
