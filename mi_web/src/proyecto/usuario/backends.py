from django.shortcuts import get_object_or_404
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
import requests
from .api_queries import get_professor, get_student
from .models import prospecto
from .save_processes import save_profile_processes

class MicrosoftGraphBackend(BaseBackend):
    
    def authenticate(request, access_token=None):
        if not access_token:
            return None
        
        if 'user_info' in request.session:
            del request.session['user_info']
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
            tipo_user = user_data.get('jobTitle')
            id_user = user_data.get('officeLocation')
            
            if not email:
                return None

            # Buscar o crear un usuario utilizando la dirección de correo electrónico
            try:
                user = User.objects.get(email=email)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    if tipo_user == 'Estudiante':
                        estudiante_usuario = get_student(id_user)
                        estudiante_usuario["tipo"] = "estudiante"
                        request.session['user_info'] = estudiante_usuario
                    elif tipo_user == 'Profesor':
                        profesor_usuario = get_professor(id_user)
                        request.session['user_info'] = profesor_usuario
                        try:
                            prospecto_user = get_object_or_404(prospecto, identificacion=id_user)
                            if prospecto_user is not None:
                                profesor_usuario["tipo"] = "prospecto/profesor"
                        except:
                            profesor_usuario["tipo"] = "profesor"
                    elif tipo_user == 'Profesores y Estudiante':
                        profesor_usuario = get_professor(id_user)
                        profesor_usuario["tipo"] = "estudiante/profesor"
                        request.session['user_info'] = profesor_usuario
                    return user
            except User.DoesNotExist:
                # Si el usuario no existe, crear uno nuevo
                email = user_data.get('mail')
                name = user_data.get('givenName')
                lastname = user_data.get('surname')
                
                datos_estados = [id_user, True, False, 'ER', True, True]
                
                #Busqueda de usuario
                if tipo_user == 'Estudiante':
                    estudiante_usuario = get_student(id_user)
                    user = User.objects.create_user(username=estudiante_usuario.get('identificacion'), email=email, first_name=name, last_name=lastname)
                    if user is not None:
                        # Guarda el nombre completo del usuario en el perfil de usuario
                        # Almacenar la información en la sesión del usuario
                        request.session['user_info'] = estudiante_usuario
                        estudiante_usuario["tipo"] = "estudiante"
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        save_profile_processes.save_user_status(request, datos_estados)
                        return user
                elif tipo_user == 'Profesor':
                    profesor_usuario = get_professor(id_user)
                    user = User.objects.create_user(username=profesor_usuario.get('identificacion'), email=email, first_name=name, last_name=lastname)
                    if user is not None:
                        # Guarda el nombre completo del usuario en el perfil de usuario
                        try:
                            prospecto_user = get_object_or_404(prospecto, identificacion=id_user)
                            if prospecto_user is not None:
                                profesor_usuario["tipo"] = "prospecto/profesor"
                        except:
                            profesor_usuario["tipo"] = "profesor"
                        request.session['user_info'] = profesor_usuario
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        return user
                elif tipo_user == 'Profesores y Estudiante':
                    profesor_usuario = get_professor(id_user)
                    user = User.objects.create_user(username=profesor_usuario.get('identificacion'), email=email, first_name=name, last_name=lastname)
                    if user is not None:
                        # Guarda el nombre completo del usuario en el perfil de usuario
                        profesor_usuario["tipo"] = "estudiante/profesor"
                        request.session['user_info'] = profesor_usuario
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        save_profile_processes.save_user_status(request, datos_estados)
                        return user