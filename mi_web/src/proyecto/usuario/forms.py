from django import forms
from .models import estudiantes, usuarios, profesor, info_estudiantes, prospecto, primerIngreso
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

class FormularioUsuario(forms.ModelForm):
    class Meta:
        model = usuarios
        fields = ('auth_user', 'activo', 'es_profesor', 'es_estudiante', 'es_prospecto', 'es_cursolibre')
        
class FormularioProspecto(forms.ModelForm):
    class Meta:
        model = prospecto
        fields = ('user','identificacion', 'nombre', 'primer_apellido','segundo_apellido', 'fecha_nacimiento', 'numero_telefonico', 
                  'numero_telefonico2', 'correo_institucional', 'correo_personal', 'nacionalidad', 'provincia', 'canton', 'distrito', 'sexo')
         

class FormularioEstudiantes(forms.ModelForm):
    class Meta:
        model = estudiantes
        fields = ('identificacion', 'nombre', 'primer_apellido','segundo_apellido', 'fecha_nacimiento', 'numero_telefonico', 
                  'numero_telefonico2', 'correo_institucional', 'correo_personal', 'nacionalidad', 'provincia', 'canton', 'distrito', 'sexo')
        
class FormularioProfesor(forms.ModelForm):
    class Meta:
        model = profesor
        fields = ('identificacion', 'nombre', 'primer_apellido','segundo_apellido', 'fecha_nacimiento', 'numero_telefonico', 
                  'numero_telefonico2', 'correo_institucional', 'correo_personal', 'nacionalidad', 'provincia', 'canton', 'distrito', 'sexo', 'puesto_educativo')
        
class FormularioInfoEstudiante(forms.ModelForm):
    class Meta:
        model = info_estudiantes
        fields = ('user','ingresoeconomico', 'carrera', 'colegio')
        
class FormularioPrimerIngreso(forms.ModelForm):
    class Meta:
        model = primerIngreso
        fields = ('etapa','estado', 'usuario', 'comentario')