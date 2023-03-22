from audioop import max

from django.db import models
from django.contrib.auth.models import User



# class Tarea(models.Model):
#     usuario = models.ForeignKey(User,
#                                 on_delete=models.CASCADE,
#                                 null=True,
#                                 blank=True)
#     titulo = models.CharField(max_length=200)
#     descripcion = models.TextField(null=True,
#                                    blank=True)
#     completo = models.BooleanField(default=False)
#     creado = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.titulo
#
#     class Meta:
#         ordering = ['completo']
#
class usuarios(models.Model):
    #id = models.AutoField(primary_key=True)
    Tipo = models.CharField(max_length=200)
    estado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    usuarios = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    class Meta:
        db_table = 'usuario_usuarios'


class estudiantes(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    Cedula = models.CharField(max_length=22)
    nombre = models.CharField(max_length=18)
    primer_apellido = models.CharField(max_length=18)
    segundo_apellido = models.CharField(max_length=18)
    fecha_nacimiento = models.DateField()
    phone_tutor = models.IntegerField(default=0)
    correo_estudiante = models.CharField(max_length=60)
    password = models.CharField(max_length=30)
    pago_realizado = models.BooleanField(default=False)
    documentos_presentados = models.BooleanField(default=False)
    user = models.OneToOneField(usuarios,on_delete=models.CASCADE)


class profesor(models.Model):
    id_profesor= models.AutoField(primary_key=True)
    Cedula = models.CharField(max_length=25)
    nombre = models.CharField(max_length=18)
    primer_apellido = models.CharField(max_length=18)
    segundo_apellido = models.CharField(max_length=18)
    correo_profesor = models.CharField(max_length=100)
    puesto_educativo = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    user = models.OneToOneField(usuarios, on_delete=models.CASCADE)



# def create_profile(sender,**kwargs):
#     if kwargs['created']:
#         if kwargs['tipo'] == 1:
#             user_profile = profesor.objects.create(user=kwargs['profesor'])
#         elif kwargs['tipo'] == 2 :
#             user_profile = estudiantes.objects.create(user=kwargs['estudiantes'])
#         else:
#             user_profile =estudiante_prospecto.objects.create(user=['estudiante_prospecto'])

# class aula_prestamos(models.Model):
#     name = models.CharField(max_length=50)
#     videobeam = models.BooleanField()
#     iftieneCpU = models.BooleanField()
#     aire = models.BooleanField()
#     llave = models.BooleanField()
#     descripcion = models.TextField()
#     ubicacion = models.CharField(max_length=50)
#     prestado = models.BooleanField()
#     aula = models.BooleanField()
