from django import forms
from .models import estudiantes, usuarios, profesor

class FormularioUsuario(forms.ModelForm):
    class Meta:
        model = usuarios
        fields = ('Tipo', 'estado', 'usuarios')

class FormularioEstudiantes(forms.ModelForm):
    class Meta:
        model = estudiantes
        fields = ('Cedula', 'nombre', 'primer_apellido','segundo_apellido', 'fecha_nacimiento', 'phone_tutor', 
                  'correo_estudiante', 'password', 'pago_realizado','documentos_presentados', 'user')
        
class FormularioProfesor(forms.ModelForm):
    class Meta:
        model = profesor
        fields = ('Cedula', 'nombre', 'primer_apellido','segundo_apellido',
                  'correo_profesor', 'puesto_educativo', 'password', 'user')