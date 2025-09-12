from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms_password_reset import PasswordResetForm

def password_reset_confirm(request, user_id, token):
    user = get_object_or_404(User, pk=user_id)
    # Validación simple del token (en producción usa PasswordResetTokenGenerator)
    if not user.password.startswith(token):
        messages.error(request, 'El enlace de recuperación no es válido o ha expirado.')
        return redirect('login')
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, '¡Contraseña restablecida correctamente! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'core/password_reset_confirm.html', {'form': form, 'user': user})
