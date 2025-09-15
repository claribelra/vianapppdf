# Manual Técnico Vianapp

## Índice
- [Dependencias del proyecto](#dependencias-del-proyecto)
- [Instalación y despliegue](#instalación-y-despliegue)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Mantenimiento y pruebas](#mantenimiento-y-pruebas)
- [Solución de problemas comunes](#solución-de-problemas-comunes)
- [Contacto y soporte](#contacto-y-soporte)
- [Fecha de actualización](#fecha-de-actualización)

---

## Dependencias del proyecto
A continuación se enumeran las principales dependencias utilizadas en el proyecto Vianapp:

1. **Django**: Framework principal para desarrollo web.
2. **Pillow**: Manejo y procesamiento de imágenes (fotos de parqueaderos y usuarios).
3. **django-crispy-forms**: Formularios modernos y personalizables.
4. **django-widget-tweaks**: Personalización de widgets en formularios.
5. **sqlite3**: Base de datos por defecto para desarrollo y pruebas.
6. **requests**: Realización de peticiones HTTP (si se usan APIs externas).
7. **gunicorn**: Servidor WSGI para despliegue en producción (opcional).
8. **whitenoise**: Gestión de archivos estáticos en producción (opcional).
9. **django-extensions**: Herramientas adicionales para desarrollo (opcional).
10. **geopy**: Geolocalización y manejo de coordenadas (si se usan mapas avanzados).

> Para instalar todas las dependencias, usar el archivo `requirements.txt` incluido en el proyecto.

---

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

## Nota sobre escalabilidad y base de datos
Si el proyecto crece y requiere manejar grandes volúmenes de datos, usuarios o transacciones, se recomienda migrar la base de datos de SQLite a una solución más robusta como MySQL o PostgreSQL. Puedes gestionar y administrar estas bases de datos fácilmente con herramientas como **MySQL Workbench** o **pgAdmin**.

Para migrar:
- Configura el motor de base de datos en `settings.py`.
- Instala el conector correspondiente (`mysqlclient` para MySQL, `psycopg2` para PostgreSQL).
- Realiza las migraciones con `python3 manage.py migrate`.
- Usa herramientas gráficas como MySQL Workbench para administración avanzada.

## Contacto y soporte
Para soporte técnico o dudas, contactar al administrador del sistema o escribir a soporte@vianapp.com.

---

## Fecha de actualización
15 de septiembre de 2025
