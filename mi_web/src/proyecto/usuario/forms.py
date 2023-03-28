from django import forms
from .models import estudiantes, usuarios, profesor, info_estudiantes
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class FormularioUsuario(forms.ModelForm):
    class Meta:
        model = usuarios
        fields = ('usuarios', 'activo', 'es_profesor', 'es_estudiante', 'es_prospecto', 'es_cursolibre')

class FormularioEstudiantes(forms.ModelForm):
    class Meta:
        model = estudiantes
        fields = ('user','identificacion', 'nombre', 'primer_apellido','segundo_apellido', 'fecha_nacimiento', 'numero_telefonico', 
                  'correo_institucional', 'correo_personal', 'direccion')
        
class FormularioProfesor(forms.ModelForm):
    class Meta:
        model = profesor
        fields = ('user','identificacion', 'nombre', 'primer_apellido','segundo_apellido','correo', 'puesto_educativo')
        
class FormularioInfoEstudiante(forms.ModelForm):
    class Meta:
        model = info_estudiantes
        fields = ('user','estado', 'carrera')
        