from django import forms
from .models import estudiantes, usuarios, profesor

class FormularioUsuario(forms.ModelForm):
    class Meta:
        model = usuarios
        fields = ('usuarios', 'activo', 'es_profesor', 'es_estudiante', 'es_prospecto')

class FormularioEstudiantes(forms.ModelForm):
    class Meta:
        model = estudiantes
        fields = ('user','identificacion', 'nombre', 'primer_apellido','segundo_apellido', 'fecha_nacimiento', 'numero_telefonico', 
                  'correo')
        
class FormularioProfesor(forms.ModelForm):
    class Meta:
        model = profesor
        fields = ('user','identificacion', 'nombre', 'primer_apellido','segundo_apellido','correo', 'puesto_educativo')