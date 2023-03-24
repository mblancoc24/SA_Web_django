from audioop import max

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
    correo = models.CharField(max_length=60)


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
    