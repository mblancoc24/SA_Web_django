# backends.py
from django.shortcuts import get_object_or_404
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
import requests
from .models import usuarios, profesor, estudiantes, RegistroLogsUser, documentos, carreras, colegios, posgrados, fotoperfil, estados, etapas, primerIngreso, prospecto
from .forms import FormularioEstudiantes, FormularioUsuario, FormularioDocumentos, FormularioPrimerIngreso, FormularioProfesor, FormularioProspecto, FormularioInfoEstudiante, CustomUserCreationForm



class MicrosoftGraphBackend(BaseBackend):
    global tipo_usuario
    tipo_usuario = ''
    
    def authenticate(request, access_token=None):
        if not access_token:
            return None

        # Obtener información del usuario utilizando Microsoft Graph API
        url = 'https://graph.microsoft.com/v1.0/me'
        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.get(url, headers=headers)
        
        # Inicia sesión en la aplicación utilizando el nuevo usuario
        if response.status_code != 200:
            return None
        else:
            # Analizar la respuesta JSON
            user_data = response.json()
            email = user_data.get('mail')

            if not email:
                return None

            # Buscar o crear un usuario utilizando la dirección de correo electrónico
            try:
                user = User.objects.get(email=email)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    return user
                else:
                    user_data = response.json()
                    email = user_data.get('mail')
                    name = user_data.get('givenName')
                    lastname = user_data.get('surname')
                    tipo_user = user_data.get('jobTitle')
                    
                    #Busqueda de usuario
                    if tipo_user == 'Estudiante':
                        estudiante_usuario = get_object_or_404(estudiantes, correo_institucional=email)
                        user, created = User.objects.create_user(username=estudiante_usuario.identificacion, email=email, first_name=name, last_name=lastname)
                        if created:
                            # Guarda el nombre completo del usuario en el perfil de usuario
                            # user.profile.full_name = name
                            # user.profile.save()
                            user.backend = 'django.contrib.auth.backends.ModelBackend'
                            return user
                    elif tipo_user == 'Profesores':
                        profesor_usuario = get_object_or_404(profesor, correo_institucional=email)
                        user, created = User.objects.create_user(username=profesor_usuario.identificacion, email=email, first_name=name, last_name=lastname)
                        if created:
                            # Guarda el nombre completo del usuario en el perfil de usuario
                            # user.profile.full_name = name
                            # user.profile.save()
                            user.backend = 'django.contrib.auth.backends.ModelBackend'
                            return user
            except User.DoesNotExist:
                # Si el usuario no existe, crear uno nuevo
                user = User.objects.create_user(username=email, email=email)
                return None
    
    def type_user(request, access_token=None):
        if not access_token:
            return None

        # Obtener información del usuario utilizando Microsoft Graph API
        url = 'https://graph.microsoft.com/v1.0/me'
        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.get(url, headers=headers)
        
        # Inicia sesión en la aplicación utilizando el nuevo usuario
        if response.status_code != 200:
            return None
        else:
            user_data = response.json()
            tipo_user = user_data.get('jobTitle')
            return tipo_user
