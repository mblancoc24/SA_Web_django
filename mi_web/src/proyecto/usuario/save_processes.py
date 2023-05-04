from .forms import FormularioEstudiantes, FormularioDocumentos, FormularioPrimerIngreso, FormularioProfesor, FormularioProspecto, FormularioInfoEstudiante, CustomUserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import profesor, estudiantes, RegistroLogsUser, documentos, carreras, colegios, posgrados, fotoperfil, estados, etapas, primerIngreso, prospecto

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
        form = FormularioPrimerIngreso({ 'etapa': data1[0], 'estado': data1[1], 
                    'convalidacion': data1[2],'usuario': data1[3],'comentario': data1[4]})
        
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
        
        form = FormularioPrimerIngreso({'etapa': data1[0], 'estado': data1[1], 'convalidacion': data1[2],
                'usuario': data1[3], 'comentario': data1[4]}, instance=statusgeneral)
        
        if form.is_valid():
            form.save()
            
        form = FormularioDocumentos({'usuario': data2[0], 'tituloeducacion': data2[1],
                                 'titulouniversitario': data2[2], 'identificacion': data2[3],
                                 'foto': data2[4], 'notas': data2[5],
                                 'plan': data2[6]}, instance=docs)

        if form.is_valid():
            form.save()
            
    def save_profile_photo(request, photo):
        user = request.user

        img_data = photo.read()

        # Convertir la imagen a bytes
        img_bytes = bytearray(img_data)

        # Crear el objeto UserFile y guardarlo en la base de datos
        user_file = fotoperfil(user=user, archivo=img_bytes)
        user_file.save()