# 🛍️ WM-Backend

Bienvenidos al proyecto **wm-backend**, el backend desarrollado con Django para gestionar toda la lógica de servidor de la aplicación **WM**.

---

## 📋 Requisitos Previos

- [Python 3.10+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)
- (Opcional) [Virtualenv](https://virtualenv.pypa.io/en/latest/) o `venv` para entorno virtual

---

## 🚀 Instalación y Ejecución

Sigue los pasos a continuación para levantar el proyecto en tu máquina local:

### 1. Clonar el repositorio

```bash
https://github.com/DylanFarkas/wm-backend.git
```

```bash
cd moda-chic-backend
```

### 2. Crear entorno virtual y activarlo

#### En Windows
```bash
python -m venv venv
```

- #### En Windows

```bash
venv/scripts/activate
```

- #### En Linux / Mac

```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configuración de la base de datos

Asegúrate de tener PostgreSQL instalado y configurado. Utiliza la siguiente configuración en tu archivo `settings.py` de Django:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'TU_HOST',           # Por ejemplo: 'localhost'
        'PORT': 'TU_PUERTO',         # Por ejemplo: '5432'
        'NAME': 'NOMBRE_BASE_DATOS', # Por ejemplo: 'modachic_db'
        'USER': 'TU_USUARIO',        # Por ejemplo: 'postgres'
        'PASSWORD': 'TU_CONTRASEÑA', # Por ejemplo: 'postgres'
    }
}
```

### 5. Aplicar migraciones

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### 6. Crear superusuario de Django

Para acceder al panel de administración de Django y gestionar modelos como productos, categorías, usuarios, etc., necesitas crear un **superusuario**. Este usuario tendrá todos los permisos y podrá acceder a la interfaz de administración web (`/admin`).

```bash
python manage.py createsuperuser
```

### 7. Correr el servidor

```bash
python manage.py runserver
```