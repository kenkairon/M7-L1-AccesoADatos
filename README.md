# M7-L1-AccesoADatos
Educativo y de Aprendizaje Personal
---
## Tabla de Contenidos
- [Tecnologías](#Tecnologías)
- [Configuración Inicial](#configuración-Inicial)
- [Configuración Base de datos](#configuración-Base-de-datos)
- [Creación del Modelo](#creación-del-modelo)
- [Creación de Vistas](#creación-de-vistas)
- [Creación de Superusuario](#creación-de-superusuario)
---
# Tecnologías
- Django: Framework web en Python.
- SQLite: Base de datos por defecto.
- PostgreSQL: Base de datos relacional avanzada (opcional).
- MongoDB: Base de datos NoSQL (opcional).
--- 
# Configuración Inicial 
1. Entorno virtual 
    ```bash 
    python -m venv venv

2. Activar el entorno virtual
    ```bash 
    venv\Scripts\activate

3. Instalar Django
    ```bash 
    pip install django 

4. Actulizamos el pip 
    ```bash
    python.exe -m pip install --upgrade pip

5. Crear el proyecto de django
    ```bash 
    django-admin startproject proyecto_educacional 

6. Ingresamos al proyecto proyecto_educacional 
    ```bash 
    cd projecto_educacional

7. Creamos la aplicacion llamada escuela
    ```bash 
    python manage.py startapp escuela

8. Configuración de proyecto_educacional/settings.py 
    ```bash 
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'escuela',
    ]

# Configuración Base de datos
9. Instalar python-decouple: Es una biblioteca que ayuda manejar las variables de entorno 
    ```bash
    pip install python-decouple

10. Creamos el archivo .env a la altura del proyecto al lado manage.py 
    ```bash
    DATABASE_NAME=nombre_base_de_datos
    DATABASE_USER=postgres
    DATABASE_PASSWORD=yourpassword
    DATABASE_HOST=localhost
    DATABASE_PORT=5432

11. Configuracion de la base de datos ingresando los parametros de conexión 
    ```bash
    from decouple import config

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD'),
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT'),
        }
    }
11. Instalacion de psycopg2: es un adaptador de base de datos para Python que permite interactuar con bases de datos PostgreSQL
    ```bash
    pip install pyscopg2 

# Creación del Modelo 

12. en escuela/models.py
    ```bash
    from django.db import models

    class Estudiante(models.Model):
        nombre = models.CharField(max_length=100)
        apellido = models.CharField(max_length=100)
        correo_electronico = models.EmailField(unique=True)
        edad = models.IntegerField()
        fecha_inscripcion = models.DateField(auto_now_add=True)

        def __str__(self):
            return f"{self.nombre} {self.apellido}"

    class Curso(models.Model):
        nombre = models.CharField(max_length=200)
        descripcion = models.TextField()
        estudiantes = models.ManyToManyField(Estudiante, related_name='cursos')

        def __str__(self):
            return self.nombre

13. Ejecuta las migraciones para aplicar estos cambios a la base de datos:
    ```bash 
    python manage.py makemigrations
    python manage.py migrate

# Creación de Vistas

14. escuela/views.py 
    ```bash 
    from django.shortcuts import render
    from django.db import connection
    from .models import Estudiante

    # Consultas personalizadas con SQL
    def consulta_sql_personalizada(request):
        # Ejecutar consulta SQL directa
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre, edad FROM escuela_estudiante WHERE edad >= %s", [18])
            columnas = [col[0] for col in cursor.description]  # Obtener los nombres de las columnas
            filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]  # Convertir a diccionario
            
        # Renderizar el resultado en una plantilla
        return render(request, 'estudiantes.html', {'estudiantes': filas})


    def ejemplo_consulta_raw(request):
        # Usar consultas SQL crudas con el ORM de Django
        estudiantes = Estudiante.objects.raw('SELECT * FROM escuela_estudiante WHERE edad >= %s', [18])
        return render(request, 'estudiantes.html', {'estudiantes': estudiantes})

15. creamos en escuela/templates/estudiantes.html 
    ```bash 
    <!DOCTYPE html>
    <html>

    <head>
        <title>Estudiantes</title>
    </head>

    <body>
        <h1>Lista de Estudiantes</h1>
        <ul>
            {% for estudiante in estudiantes %}
            <li>{{ estudiante }}</li>
            {% endfor %}
        </ul>
    </body>

    </html>
16. proyecto_educacional/settings.py 
    ```bash 
    from django.contrib import admin
    from django.urls import path
    from escuela import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('consulta1/', views.consulta_sql_personalizada, name='custom_query'),
        path('consulta2/', views.ejemplo_consulta_raw, name='raw_query'),
    ]
# Creación de Superusuario

17. Creacion del superusuario
    ```bash	
    python manage.py createsuperuser

18. Se Crea un contraseña solo para fines pedagogicos y para ir testeando el modelo 
    ```bash	
    admin
    admin1234
    y

19. En escuela/admin.py 
    ```bash	
    from django.contrib import admin
    from .models import Curso, Estudiante

    admin.site.register(Curso)
    admin.site.register(Estudiante)


