from .forms import FormularioEstudiantes, FormularioDocumentos, FormularioPrimerIngreso, FormularioProfesor, FormularioProspecto, FormularioInfoEstudiante, CustomUserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import profesor, estudiantes, RegistroLogsUser, documentos, carreras, colegios, posgrados, fotoperfil, estados, primerIngreso, prospecto

class save_profile_processes():
    
    def save_prospecto(request, data):
        form = FormularioProspecto({'identificacion': data[0], 'nombre': data[1], 'primer_apellido': data[2],
                'segundo_apellido': data[3], 'fecha_nacimiento': data[4], 'numero_telefonico': data[5], 'numero_telefonico2': data[6],
                'correo_institucional': data[7], 'correo_personal': data[8], 'nacionalidad': data[9], 'provincia': data[10],
                'canton': data[11], 'distrito': data[12], 'sexo': data[13]})
            
        if form.is_valid():
            form.save()
            return True
        else:
            return False
        
    def update_professor(request, data):
        user = request.user
        user = User.objects.get(username=user.username)
        
        profesores = get_object_or_404(profesor, identificacion=user.username)
        
        form = FormularioProfesor({'identificacion': data[0], 'nombre': data[1], 'primer_apellido': data[2],'segundo_apellido': data[3], 
                    'fecha_nacimiento': data[4], 'numero_telefonico': data[5], 'numero_telefonico2': data[6],
                    'correo_institucional': data[7], 'correo_personal': data[8], 'nacionalidad': data[9], 'provincia': data[10],
                    'canton': data[11], 'distrito': data[12], 'sexo': data[13], 'puesto_educativo': data[14]}, instance=profesores)
        
        if form.is_valid():
            form.save()
            return True
        else:
            return False
    
    def update_student(request, data):
        user = request.user
        user = User.objects.get(username=user.username)
        
        estudiante = get_object_or_404(estudiantes, identificacion=user.username)
        
        form = FormularioEstudiantes({'identificacion': data[0], 'nombre': data[1], 'primer_apellido': data[2],
                    'segundo_apellido': data[3], 'fecha_nacimiento': data[4], 'numero_telefonico': data[5], 'numero_telefonico2': data[6],
                    'correo_institucional': data[7], 'correo_personal': data[8], 'nacionalidad': data[9], 'provincia': data[10],
                    'canton': data[11], 'distrito': data[12], 'sexo': data[13]}, instance=estudiante)

        if form.is_valid():
            form.save()
            return True
        else:
            return False
        
    def update_prospecto(request, data):
        user = request.user
        user = User.objects.get(username=user.username)
        
        prospecto_user = get_object_or_404(prospecto, identificacion=user.username)
        
        form = FormularioProspecto({'identificacion': data[0], 'nombre': data[1], 'primer_apellido': data[2],
                    'segundo_apellido': data[3], 'fecha_nacimiento': data[4], 'numero_telefonico': data[5], 'numero_telefonico2': data[6],
                    'correo_institucional': data[7], 'correo_personal': data[8], 'nacionalidad': data[9], 'provincia': data[10],
                    'canton': data[11], 'distrito': data[12], 'sexo': data[13]}, instance=prospecto_user)

        if form.is_valid():
            form.save()
            return True
        else:
            return False
    
    def save_documents(request, data1, data2):
        form = FormularioPrimerIngreso({'estado': data1[0], 
                    'convalidacion': data1[1],'comentario': data1[2],'usuario': data1[3]})
        
        if form.is_valid():
            form.save()
        
        form = FormularioDocumentos({'usuario': data2[0], 'tituloeducacion': data2[1],
                'titulouniversitario': data2[2], 'identificacion': data2[3],
                'foto': data2[4], 'notas': data2[5],'plan': data2[6]})

        if form.is_valid():
            form.save()
            return True
        else:
            return False
    
    def update_documents(request, data1, data2):
        user = request.user
        
        statusgeneral = get_object_or_404(primerIngreso, usuario=user.pk)
        docs = get_object_or_404(documentos, usuario=user.pk)
        
        form = FormularioPrimerIngreso({'estado': data1[0], 'convalidacion': statusgeneral.convalidacion,
                                        'comentario': data1[4],'usuario': user.pk}, instance=statusgeneral)
        
        if form.is_valid():
            form.save()
            
        form = FormularioDocumentos({'usuario': user.pk, 'tituloeducacion': data2[1],
                'titulouniversitario': docs.titulouniversitario, 'identificacion': data2[3],
                'foto': data2[4], 'notas': data2[5],'plan': data2[6]}, instance=docs)

        if form.is_valid():
            form.save()
            return True
        else:
            return False
            
    def update_user_prospecto(data):
        user = User.objects.filter(username=data[0])
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
                    prospecto_user1.delete()
                    user = User.objects.get(email=usuario1["email"])
                    user.delete()
            except:
                try:
                    prospecto_user2 = get_object_or_404(prospecto, correo_personal=usuario2["email"])
                    if prospecto_user2 is not None:
                        prospecto_user2.delete()
                        user = User.objects.get(email=usuario2["email"])
                        user.delete()
                        
                except:
                    return False
        elif usuario1 is not None:
            user = User.objects.get(email=usuario1["email"])
            user.email = data[1]
            user.save()
            
            user_prospecto = prospecto.objects.get(id_prospecto=user.username)
            user_prospecto.delete()
            return True
    
    def save_photo_perfil(request, photo):
        user = request.user
        fotoperfil_instancia = fotoperfil()
        fotoperfil_instancia.user = user
        fotoperfil_instancia.archivo = photo.read()
        fotoperfil_instancia.save()
        return True