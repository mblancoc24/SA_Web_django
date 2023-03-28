from django.contrib import admin
from .models import estudiantes, profesor, carreras

# admin.site.register(usuarios)
admin.site.register(estudiantes)
admin.site.register(profesor)
admin.site.register(carreras)