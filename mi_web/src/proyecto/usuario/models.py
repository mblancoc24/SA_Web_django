from audioop import max
from django import forms
from django.db import models
from django.contrib.auth.models import User

class usuarios(models.Model):
    usuarios = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    activo = models.BooleanField(default=False)
    es_profesor = models.BooleanField(default=False)
    es_estudiante = models.BooleanField(default=False)
    es_prospecto = models.BooleanField(default=True)
    es_cursolibre = models.BooleanField(default=False)
    fecha_creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuarios

class estudiantes(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    user = models.OneToOneField(usuarios,on_delete=models.CASCADE)
    identificacion = models.CharField(max_length=22)
    nombre = models.CharField(max_length=18)
    primer_apellido = models.CharField(max_length=18)
    segundo_apellido = models.CharField(max_length=18)
    fecha_nacimiento = models.DateField()
    numero_telefonico = models.IntegerField(default=0)
    correo_institucional = models.CharField(max_length=60)
    correo_personal = models.CharField(max_length=60)
    direccion = models.CharField(max_length=200)
    
    
class info_estudiantes (models.Model):
    id_info = models.AutoField(primary_key=True)
    user = models.OneToOneField(estudiantes, on_delete=models.CASCADE)
    estado = models.CharField(max_length=25)
    carrera = models.CharField(max_length=300)


class profesor(models.Model):
    id_profesor= models.AutoField(primary_key=True)
    user = models.OneToOneField(usuarios, on_delete=models.CASCADE)
    identificacion = models.CharField(max_length=25)
    nombre = models.CharField(max_length=18)
    primer_apellido = models.CharField(max_length=18)
    segundo_apellido = models.CharField(max_length=18)
    correo = models.CharField(max_length=100)
    puesto_educativo = models.CharField(max_length=50)
    
class RegistroLogsUser (models.Model):
    fechatiempo = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=300)
    
class RegistroIDUserCambios (models.Model):
    fechatiempo = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_ident_nueva = models.CharField(max_length=25)
    nueva_identificacion = models.CharField(max_length=25)
    antigua_identifiacion = models.CharField(max_length=25)
    tipo_ident_antigua = models.CharField(max_length=25)
    
class carreras (models.Model):
    id = models.AutoField(primary_key=True)
    nombre_carrera = models.CharField(max_length=60)
    
    class Meta:
        db_table = 'carreras'

class colegios (models.Model):
    nombre_colegio = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = 'colegios'