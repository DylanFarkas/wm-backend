#!/usr/bin/env bash
set -e

echo "🚀 Iniciando despliegue del backend Django..."

# Aplicar migraciones
echo "📦 Aplicando migraciones..."
python manage.py migrate --noinput

# Crear superusuario automáticamente si no existe
echo "👤 Verificando superusuario..."
python manage.py shell << END
import os
from django.contrib.auth import get_user_model
User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@gmail.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123*")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superusuario creado: {username} / {password}")
else:
    print(f"ℹ️ El superusuario '{username}' ya existe.")
END

# Recolectar archivos estáticos (por si no se ejecutó en el build)
echo "🎨 Ejecutando collectstatic..."
python manage.py collectstatic --noinput

# Iniciar el servidor con Gunicorn
echo "🔥 Iniciando servidor Gunicorn..."
exec gunicorn wm_api.wsgi:application --workers=3 --threads=4 --timeout=120
