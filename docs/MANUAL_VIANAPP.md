# Manual de Usuario y Manual Técnico

## Índice
- [Manual de Usuario](#manual-de-usuario)
  - [Administrador](#administrador)
  - [Cliente](#cliente)
  - [Parqueadero](#parqueadero)
- [Manual Técnico](#manual-técnico)
  - [Instalación y despliegue](#instalación-y-despliegue)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Mantenimiento y pruebas](#mantenimiento-y-pruebas)
  - [Solución de problemas comunes](#solución-de-problemas-comunes)

---

# Manual de Usuario

## Administrador
### Funcionalidades principales
- Acceso al dashboard administrativo.
- Gestión de usuarios (clientes y parqueaderos).
- Visualización y edición de información de parqueaderos.
- Acceso a estadísticas y reportes.
- Gestión de valoraciones y comentarios.

### Instrucciones de uso
1. Iniciar sesión con usuario administrador.
2. Navegar al dashboard desde el menú principal.
3. Usar los accesos directos para gestionar usuarios y parqueaderos.
4. Editar información relevante y guardar cambios.
5. Consultar reportes y estadísticas desde el panel.

### Recomendaciones
- Verificar los cambios antes de guardar.
- Utilizar los filtros para encontrar usuarios o parqueaderos rápidamente.
- Revisar periódicamente las valoraciones y comentarios para mantener la calidad del servicio.

---

## Cliente
### Funcionalidades principales
- Registro y acceso al sistema.
- Visualización de parqueaderos en el mapa.
- Realización y cancelación de reservas.
- Consulta de tarifas y cupos disponibles.
- Valoración y comentarios sobre parqueaderos.

### Instrucciones de uso
1. Registrarse como cliente y completar el perfil.
2. Iniciar sesión y acceder al dashboard de cliente.
3. Buscar parqueaderos en el mapa y consultar detalles.
4. Realizar reservas y cancelarlas si es necesario.
5. Valorar y comentar sobre el servicio recibido.

### Recomendaciones
- Cancelar reservas que no se vayan a utilizar para liberar cupos.
- Revisar las tarifas antes de reservar.
- Utilizar el sistema de valoraciones para mejorar la experiencia de otros usuarios.

---

## Parqueadero
### Funcionalidades principales
- Registro y asociación automática del parqueadero al perfil.
- Edición de tarifas por hora/día y cupos disponibles.
- Visualización y gestión de reservas activas.
- Acceso a dashboard con información relevante.
- Recepción de valoraciones y comentarios.

### Instrucciones de uso
1. Registrarse como parqueadero y completar el formulario con datos reales.
2. Iniciar sesión y acceder al dashboard de parqueadero.
3. Editar tarifas y cupos desde el panel y guardar cambios.
4. Consultar reservas activas y cancelarlas si es necesario.
5. Revisar valoraciones y comentarios para mejorar el servicio.

### Recomendaciones
- Mantener actualizada la información de tarifas y cupos.
- Responder a comentarios y valoraciones para mejorar la reputación.
- Utilizar el dashboard para monitorear la ocupación y optimizar el negocio.

---

# Manual Técnico

## Instalación y despliegue
1. Clonar el repositorio y ubicarse en la raíz del proyecto.
2. Crear y activar un entorno virtual:
   ```zsh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instalar dependencias:
   ```zsh
   pip install -r requirements.txt
   ```
4. Aplicar migraciones:
   ```zsh
   python3 manage.py migrate
   ```
5. Crear superusuario si es necesario:
   ```zsh
   python3 manage.py createsuperuser
   ```
6. Ejecutar el servidor:
   ```zsh
   python3 manage.py runserver
   ```

## Estructura del proyecto
- `core/`: Lógica principal, modelos, vistas, formularios, templates.
- `dashboard_admin/`: Panel administrativo y funcionalidades avanzadas.
- `static/`: Archivos estáticos (CSS, imágenes, videos).
- `templates/`: Plantillas HTML para cada módulo.
- `db.sqlite3`: Base de datos por defecto.
- `manage.py`: Script principal de gestión de Django.

## Mantenimiento y pruebas
- Para limpiar la base de datos y dejar solo usuarios de prueba, ejecutar:
  ```zsh
  python3 manage.py shell
  exec(open('core/tests.py').read())
  ```
- Para ejecutar pruebas automáticas:
  ```zsh
  python3 manage.py test
  ```
- Para actualizar dependencias:
  ```zsh
  pip install --upgrade -r requirements.txt
  ```

## Solución de problemas comunes
- **Puerto 8000 ocupado:**
  ```zsh
  lsof -i :8000
  kill -9 <PID>
  ```
- **Errores de migración:**
  ```zsh
  python3 manage.py makemigrations
  python3 manage.py migrate
  ```
- **Problemas con dependencias:**
  ```zsh
  pip install -r requirements.txt
  ```
- **Recuperar contraseña de usuario:**
  Usar la funcionalidad de "Olvidé mi contraseña" en la pantalla de login.

---

**Contacto y soporte:**
Para soporte técnico o dudas, contactar al administrador del sistema o escribir a soporte@vianapp.com.

---

**Fecha de actualización:** 15 de septiembre de 2025
