# backends.py
from django.shortcuts import get_object_or_404
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
import requests
from .models import profesor, estudiantes, RegistroLogsUser, documentos, carreras, colegios, posgrados, fotoperfil, estados, etapas, primerIngreso, prospecto

class MicrosoftGraphBackend(BaseBackend):
    
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
                    pass
            except User.DoesNotExist:
                # Si el usuario no existe, crear uno nuevo
                user_data = response.json()
                email = user_data.get('mail')
                name = user_data.get('givenName')
                lastname = user_data.get('surname')
                tipo_user = user_data.get('jobTitle')
                    
                #Busqueda de usuario
                if tipo_user == 'Estudiante':
                    estudiante_usuario = get_object_or_404(estudiantes, correo_institucional=email)
                    user = User.objects.create_user(username=estudiante_usuario.identificacion, email=email, first_name=name, last_name=lastname)
                    if user is not None:
                        # Guarda el nombre completo del usuario en el perfil de usuario
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        return user
                elif tipo_user == 'Profesores':
                    profesor_usuario = get_object_or_404(profesor, correo_institucional=email)
                    user = User.objects.create_user(username=profesor_usuario.identificacion, email=email, first_name=name, last_name=lastname)
                    if user is not None:
                        # Guarda el nombre completo del usuario en el perfil de usuario
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        return user
    
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
        
    def user_type(request):
        user = request.user
        user = User.objects.filter(username=user.username)
        
        usuario1 = None
        usuario2 = None

        for index, usuario in enumerate(user):
            if index == 0:
                usuario1 = {
                    'id': usuario.id,
                    'username': usuario.username,
                    'email': usuario.email,
                    'first_name': usuario.first_name,
                    'last_name': usuario.last_name
                }
            else:
                usuario2 = {
                    'id': usuario.id,
                    'username': usuario.username,
                    'email': usuario.email,
                    'first_name': usuario.first_name,
                    'last_name': usuario.last_name
                }
        if usuario1 is not None and usuario2 is not None:
            
            try:
                prospecto_user1 = get_object_or_404(prospecto, correo_personal=usuario1["email"])
                if prospecto_user1 is not None:
                    type1 = 'prospecto/profesor'
            except:
                try:
                    estudiante_user1 = get_object_or_404(estudiantes, correo_institucional=usuario1["email"])
                    if estudiante_user1 is not None:
                        type1 = 'estudiante/profesor'
                except:
                    try:
                        prospecto_user2 = get_object_or_404(prospecto, correo_personal=usuario1["email"])
                        if prospecto_user2 is not None:
                            type1 = 'prospecto/profesor'
                        
                    except:
                        try:
                            estudiante_user2 = get_object_or_404(estudiantes, correo_institucional=usuario1["email"])
                            if estudiante_user2 is not None:
                                type1 = 'estudiante/profesor'
                        except:
                            type1 = 'no existe'
                
        elif usuario1 is not None:
            try:
                prospecto_user1 = get_object_or_404(prospecto, correo_personal=usuario1["email"])
                if prospecto_user1 is not None:
                    type1 = 'prospecto'
            except:
                try:
                    estudiante_user1 = get_object_or_404(estudiantes, correo_institucional=usuario1["email"])
                    if estudiante_user1 is not None:
                        type1 = 'estudiante'
                except:
                    try:
                        profesores_user1 = get_object_or_404(profesor, correo_institucional=usuario1["email"])
                        if profesores_user1 is not None:
                            type1 = 'profesor'
                    except:
                        type1 = 'no existe'
                    
        return type1
        
    def get_user_data(request, usertype):
        user = request.user
        user = User.objects.filter(username=user.username)
        
        if usertype == 'estudiante/profesor':
            data = get_object_or_404(profesor, identificacion=user.username) 
           
        elif usertype == 'prospecto/profesor':    
            data = get_object_or_404(prospecto, identificacion=user.username)
        
        elif usertype == 'profesor':
            data = get_object_or_404(profesor, identificacion=user.username)
            
        elif usertype == 'estudiante':
            data = get_object_or_404(estudiantes, identificacion=user.username)
            
        elif usertype == 'prospecto':
            data = get_object_or_404(prospecto, identificacion=user.username)
            
        return data