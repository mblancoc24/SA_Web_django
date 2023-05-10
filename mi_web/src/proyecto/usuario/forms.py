from django import forms
from .models import estudiantes, profesor, user_status, prospecto, primerIngreso, documentos
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


class FormularioProspecto(forms.ModelForm):
    class Meta:
        model = prospecto
        fields = ('identificacion', 'nombre', 'primer_apellido','segundo_apellido', 'fecha_nacimiento', 'numero_telefonico', 
                  'numero_telefonico2', 'correo_institucional', 'correo_personal', 'nacionalidad', 'provincia', 'canton', 'distrito', 'direccion_exacta', 'sexo')
         

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
        
class FormularioUserStatus(forms.ModelForm):
    class Meta:
        model = user_status
        fields = ('identificacion','activo', 'moroso', 'form', 'prematricula', 'matricula')
        
class FormularioPrimerIngreso(forms.ModelForm):
    class Meta:
        model = primerIngreso
        fields = ('estado', 'convalidacion', 'comentario', 'usuario')
        
class FormularioDocumentos(forms.ModelForm):
    class Meta:
        model = documentos
        fields = ('usuario','tituloeducacion', 'titulouniversitario', 'identificacion', 'foto', 'notas', 'plan')