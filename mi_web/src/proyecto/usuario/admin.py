from django.contrib import admin
from .models import estudiantes, profesor

# admin.site.register(usuarios)
admin.site.register(estudiantes)
admin.site.register(profesor)