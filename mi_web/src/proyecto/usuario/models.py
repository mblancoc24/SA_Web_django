from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class estudiantes(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=22)
    nombre = models.CharField(max_length=18)
    primer_apellido = models.CharField(max_length=18)
    segundo_apellido = models.CharField(max_length=18)
    fecha_nacimiento = models.DateField()
    numero_telefonico = models.IntegerField(default=0)
    numero_telefonico2 = models.IntegerField(default=0)
    correo_institucional = models.CharField(max_length=60)
    correo_personal = models.CharField(max_length=60)
    nacionalidad = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    canton = models.CharField(max_length=20)
    distrito = models.CharField(max_length=20)
    direccion_exacta = models.CharField(max_length=500)
    sexo = models.CharField(max_length=15)
    
class prospecto(models.Model):
    id_prospecto = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=22)
    nombre = models.CharField(max_length=18)
    primer_apellido = models.CharField(max_length=18)
    segundo_apellido = models.CharField(max_length=18)
    fecha_nacimiento = models.DateField()
    numero_telefonico = models.IntegerField(default=0)
    numero_telefonico2 = models.IntegerField(default=0)
    correo_institucional = models.CharField(max_length=60)
    correo_personal = models.CharField(max_length=60)
    nacionalidad = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    canton = models.CharField(max_length=20)
    distrito = models.CharField(max_length=20)
    direccion_exacta = models.CharField(max_length=500)
    sexo = models.CharField(max_length=15)
    
    
class user_status (models.Model):
    id_user_status = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=22)
    activo = models.BooleanField(default=True)
    moroso = models.BooleanField(default=False)
    form = models.CharField(max_length=2)
    prematricula = models.BooleanField(default=False)
    matricula = models.BooleanField(default=False)


class profesor(models.Model):
    id_profesor= models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=25)
    nombre = models.CharField(max_length=18)
    primer_apellido = models.CharField(max_length=18)
    segundo_apellido = models.CharField(max_length=18)
    fecha_nacimiento = models.DateField()
    numero_telefonico = models.IntegerField(default=0)
    numero_telefonico2 = models.IntegerField(default=0)
    correo_institucional = models.CharField(max_length=60)
    correo_personal = models.CharField(max_length=60)
    nacionalidad = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    canton = models.CharField(max_length=20)
    distrito = models.CharField(max_length=20)
    direccion_exacta = models.CharField(max_length=500)
    sexo = models.CharField(max_length=15)
    puesto_educativo = models.CharField(max_length=50)
    
class RegistroLogsUser (models.Model):
    fechatiempo = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True)
    accion = models.CharField(max_length=300)
    
class RegistroIDUserCambios (models.Model):
    fechatiempo = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True)
    tipo_ident_nueva = models.CharField(max_length=25)
    nueva_identificacion = models.CharField(max_length=25)
    antigua_identifiacion = models.CharField(max_length=25)
    tipo_ident_antigua = models.CharField(max_length=25)
    
class fotoperfil(models.Model):
    user = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True)
    archivo = models.BinaryField() 
    
class estados (models.Model):
    id_estado = models.AutoField(primary_key=True)
    estado_nombre = models.CharField(max_length=30)
    
class primerIngreso (models.Model):
    id_fase = models.AutoField(primary_key=True)
    estado = models.ForeignKey(estados, on_delete=models.CASCADE)
    convalidacion = models.BooleanField(default=False)
    usuario = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True)
    comentario = models.TextField(max_length=500)
    
class documentos (models.Model):
    id_documento = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True)
    tituloeducacion = models.BooleanField(default=False)
    titulouniversitario = models.BooleanField(default=False)
    identificacion = models.BooleanField(default=False)
    foto = models.BooleanField(default=False)
    notas = models.BooleanField(default=False)
    plan = models.BooleanField(default=False)
     
class posgrados (models.Model):
    nombre_carrera = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = 'posgrados'

class colegios (models.Model):
    nombre_colegio = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = 'colegios'
        
class carreras (models.Model):
    nombre_carrera = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = 'primer_ingreso'
        

        
        