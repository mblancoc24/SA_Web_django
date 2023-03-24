from audioop import max

from django.db import models
from django.contrib.auth.models import User

class usuarios(models.Model):
    usuarios = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    Tipo = models.CharField(max_length=200)
    estado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuarios

class estudiantes(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    user = models.OneToOneField(usuarios,on_delete=models.CASCADE)
    Cedula = models.CharField(max_length=22)
    nombre = models.CharField(max_length=18)
    primer_apellido = models.CharField(max_length=18)
    segundo_apellido = models.CharField(max_length=18)
    fecha_nacimiento = models.DateField()
    phone_tutor = models.IntegerField(default=0)
    correo_estudiante = models.CharField(max_length=60)
<<<<<<< HEAD
=======
    password = models.CharField(max_length=128)
>>>>>>> 6d04073f2ac9b16e94d8ca5c239fc99a65fb7bfb
    pago_realizado = models.BooleanField(default=False)
    documentos_presentados = models.BooleanField(default=False)


class profesor(models.Model):
    id_profesor= models.AutoField(primary_key=True)
    user = models.OneToOneField(usuarios, on_delete=models.CASCADE)
    Cedula = models.CharField(max_length=25)
    nombre = models.CharField(max_length=18)
    primer_apellido = models.CharField(max_length=18)
    segundo_apellido = models.CharField(max_length=18)
    correo_profesor = models.CharField(max_length=100)
    puesto_educativo = models.CharField(max_length=50)
    