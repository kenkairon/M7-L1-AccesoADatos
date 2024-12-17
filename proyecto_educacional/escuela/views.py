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