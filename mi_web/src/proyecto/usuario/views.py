from django.shortcuts import render, redirect, get_object_or_404
from .models import usuarios, profesor, estudiantes, RegistroLogsUser, documentos, fotoperfil, estados, etapas, primerIngreso, prospecto
from .forms import FormularioEstudiantes, FormularioUsuario, FormularioDocumentos, FormularioPrimerIngreso, FormularioProfesor, FormularioProspecto, FormularioInfoEstudiante, CustomUserCreationForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image
from odoorpc import ODOO
import base64
import threading
import xmlrpc.client
import requests
import json
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
import random
from django.urls import reverse

class Logueo(LoginView):
    template_name = 'usuario/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        logout(self.request)
        # Get the user object from the form data
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        
        # Call the parent form_valid method if the user is not authenticated
        if user is None:
            form.add_error('username', 'El usuario no existe en el sistema')
            logout(self.request)
            return super().form_invalid(form)
        
        # Authenticate the user and log them in
        login(self.request, user)
        login_obj = get_object_or_404(usuarios, auth_user=user.id)
        if login_obj.es_estudiante and login_obj.es_profesor:
            #ACA SE CONSULTARIA A LA BASE DE DATOS DE LAS CLAVES PREDETERMINADAS
            if password == 'Admin1818$':
                registrar_accion(login_obj, 'El usuario {0} ha realizado un cambio de contrasena y ha ingresado.'.format(username))
                modal = True
                return redirect('change_password')
            else:
                registrar_accion(login_obj, 'El usuario {0} ha ingresado como profesor.'.format(username))
                context = {'id': username, 'status': 3}
                return redirect(reverse('profesor', kwargs=context))
            
        elif login_obj.es_prospecto and login_obj.es_profesor:
            #ACA SE CONSULTARIA A LA BASE DE DATOS DE LAS CLAVES PREDETERMINADAS
            if password == 'Admin1818$':
                registrar_accion(login_obj, 'El usuario {0} ha realizado un cambio de contrasena y ha ingresado.'.format(username))
                modal = True
                return redirect('change_password')
            else:
                registrar_accion(login_obj, 'El usuario {0} ha ingresado como profesor.'.format(username))
                context = {'id': username, 'status': 3}
                return redirect(reverse('profesor', kwargs=context))
        else:
            if login_obj.es_prospecto:
                registrar_accion(login_obj, 'El usuario {0} ha ingresado como prospecto.'.format(username))
                context = {'id': username, 'status': 4}
                return redirect(reverse('usuario_prospecto', kwargs=context))
            
            elif login_obj.es_estudiante:
                registrar_accion(login_obj, 'El usuario {0} ha ingresado como estudiante.'.format(username))
                context = {'id': username, 'status': 1}
                return redirect(reverse('estudiante', kwargs=context))
            
            elif login_obj.es_profesor:
                registrar_accion(login_obj, 'El usuario {0} ha ingresado como profesor.'.format(username))
                #ACA SE CONSULTARIA A LA BASE DE DATOS DE LAS CLAVES PREDETERMINADAS
                if password == 'Admin1818$':
                    registrar_accion(self.request.user, 'El usuario {0} ha realizado un cambio de contrasena  y ha ingresado.'.format(username))
                    return redirect('change_password')
                else:
                    context = {'id': username, 'status': 2}
                    return redirect(reverse('profesor', kwargs=context))


class PaginaRegistroEstudiante(FormView):
    template_name = 'usuario/registro_estudiantes.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        es_profesor = self.request.POST.get('es_profesor')
        username = form.cleaned_data['username']
        nombre_estudiante = self.request.POST.get('first_name')
        primerapellido = self.request.POST.get('last_name')
        segundoapellido = self.request.POST.get('segundoapellido')
        
        if es_profesor == 'profesor':
            Usuarios = form.save() # type: ignore
             
            user = User.objects.get(username=username)
            user_id = user.pk
            
            profesor_usuario = get_object_or_404(profesor, identificacion=username)
            
            datos_usuario = [user_id, False, True, False, True, False]
            
            form = FormularioUsuario({'auth_user': datos_usuario[0],  'activo': datos_usuario[1], 'es_profesor': datos_usuario[2], 'es_estudiante': datos_usuario[3], 'es_prospecto': datos_usuario[4], 'es_cursolibre': datos_usuario[5]})
            
            if form.is_valid():
                form.save()
                
            datos_estudiante = [profesor_usuario.identificacion, profesor_usuario.nombre, profesor_usuario.primer_apellido, 
                                profesor_usuario.segundo_apellido, profesor_usuario.fecha_nacimiento, profesor_usuario.numero_telefonico, profesor_usuario.numero_telefonico2, profesor_usuario.correo_institucional, 
                                profesor_usuario.correo_personal, profesor_usuario.nacionalidad, profesor_usuario.provincia, profesor_usuario.canton, profesor_usuario.distrito, profesor_usuario.sexo]
            
            form = FormularioEstudiantes({'identificacion': datos_estudiante[0], 'nombre': datos_estudiante[1], 'primer_apellido': datos_estudiante[2],
                                        'segundo_apellido': datos_estudiante[3], 'fecha_nacimiento': datos_estudiante[4], 'numero_telefonico': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6],
                                        'correo_institucional': datos_estudiante[7], 'correo_personal': datos_estudiante[8], 'nacionalidad': datos_estudiante[9], 'provincia': datos_estudiante[10], 
                                        'canton': datos_estudiante[11], 'distrito': datos_estudiante[12], 'sexo': datos_estudiante[13]})
            if form.is_valid():
                form.save()
                
        elif es_profesor == 'estudiante' or es_profesor == 'estudianteprofesor':
            
            Usuarios = form.save() # type: ignore
            
            user = User.objects.get(username=username)
            user_id = user.pk
            
            if es_profesor == 'estudianteprofesor':
                datos_usuario = [user_id, False, True, True, False, False]
            else:
                datos_usuario = [user_id, False, False, True, False, False]
            
            form = FormularioUsuario({'auth_user': datos_usuario[0],  'activo': datos_usuario[1], 'es_profesor': datos_usuario[2], 'es_estudiante': datos_usuario[3], 'es_prospecto': datos_usuario[4], 'es_cursolibre': datos_usuario[5]})
            
            if form.is_valid():
                form.save()
                
        elif es_profesor == 'prospecto':
            fecha = self.request.POST.get('fechanacimiento')
            telefono = self.request.POST.get('telefono')
            telefono2 = self.request.POST.get('telefono2')
            correo_personal = self.request.POST.get('email')
            nacionalidad = self.request.POST.get('pais')
            provincia = self.request.POST.get('provincia')
            canton = self.request.POST.get('canton')
            distrito = self.request.POST.get('distrito')
            sexo = self.request.POST.get('Genero_select')

            Usuarios = form.save() # type: ignore
            
            user = User.objects.get(username=username)
            user_id = user.pk
            
            datos_usuario = [user_id, False, False, False, True, False]
            
            form = FormularioUsuario({'auth_user': datos_usuario[0],  'activo': datos_usuario[1], 'es_profesor': datos_usuario[2], 'es_estudiante': datos_usuario[3], 'es_prospecto': datos_usuario[4], 'es_cursolibre': datos_usuario[5]})
            
            if form.is_valid():
                form.save()
            
            usuario = get_object_or_404(usuarios, auth_user=user_id)
            id_usuario = usuario.auth_user_id
            
            datos_estudiante = [id_usuario, username, nombre_estudiante, primerapellido, 
                                segundoapellido, fecha, telefono, telefono2, 'No Asignado', correo_personal, nacionalidad, provincia, canton, distrito, sexo]
            
            form = FormularioProspecto({'user': datos_estudiante[0],'identificacion': datos_estudiante[1], 'nombre': datos_estudiante[2], 'primer_apellido': datos_estudiante[3],
                                        'segundo_apellido': datos_estudiante[4], 'fecha_nacimiento': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6], 'numero_telefonico2': datos_estudiante[7],
                                        'correo_institucional': datos_estudiante[8], 'correo_personal': datos_estudiante[9], 'nacionalidad': datos_estudiante[10], 'provincia': datos_estudiante[11], 
                                        'canton': datos_estudiante[12], 'distrito': datos_estudiante[13], 'sexo': datos_estudiante[14]})
            if form.is_valid():
                form.save()
            
        if Usuarios is not None:
            user = get_object_or_404(usuarios, auth_user=user_id)
            login(self.request, Usuarios)
            registrar_accion(user, 'El usuario '+ username +' se ha creado una cuenta como prospecto.')
            logout(self.request)
        return super(PaginaRegistroEstudiante, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
            return redirect('registro_estudiantes')
        return super(PaginaRegistroEstudiante, self).get(*args, **kwargs)

class DetalleUsuarioEstudiante(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'prueba_estudiante'
    template_name = 'Dashboard/Estudiante/prueba_estudiante.html'
      
class DetalleUsuarioProfesor(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'prueba_profesor'
    template_name = 'Dashboard/Profesor/prueba_profesor.html'


class DetalleUsuarioProspecto(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'prueba_prospecto'
    template_name = 'Dashboard/Prospecto/prospecto.html'
    
    def get(self, request, id, status):
        
        user = request.user
        usuario = get_object_or_404(usuarios, auth_user=user.pk)
        
        try:
            fotoperfil_obj = fotoperfil.objects.get(user=usuario.pk) 
            imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))
            context = {
                'id': id,
                'status': status,
                'user': user,
                'fotoperfil': imagen_url,
            }
        except fotoperfil.DoesNotExist:

            context = {
                'id': id,
                'status': status,
                'user': user,
            }
        return render(request, 'Dashboard/Prospecto/prospecto.html', context)
    
class DetalleUsuarioEstudianteProfesor(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'opciones_estudiante_profesor'
    template_name = 'usuario/opciones_login.html'
    

class DetalleArchivoOdoo(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'envio_archivos_odoo'
    template_name = 'usuario/mmgv.html'


class CrearUsuario(LoginRequiredMixin, CreateView):
    model = usuarios
    fields = ['nombre', 'primer_apellido', 'segundo_apellido','segundo_apellido']
    success_url = reverse_lazy('usuario')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearUsuario, self).form_valid(form)

def obtener_datos(request):
    id = request.GET.get("identificacion")
    url = 'https://api.hacienda.go.cr/fe/ae?identificacion=' + id
    response = requests.get(url)
    
    data_usuario = json.loads(response.text)
        
    if len(id) == 9:
        data_nombre = data_usuario["nombre"]
        if data_nombre is not None:
            nombre_completo = data_nombre.split()
            
            nombre = ' '.join(nombre_completo[:-2]).title()
            primer_apellido = nombre_completo[-2].title()
            segundo_apellido = nombre_completo[-1].title()
            
            try:
                user = get_object_or_404(profesor, identificacion=id)
                status = 'profesor'
            except:
                user = None
            
            if user is not None:
                
                try:
                    user = get_object_or_404(estudiantes, identificacion=id)
                    status = 'estudianteprofesor'
                except:
                    user = None
                
                if user is not None:
                    data = [nombre, primer_apellido, segundo_apellido, status]
                else:    
                    data = [nombre, primer_apellido, segundo_apellido, status]
                    
            else:
                try:
                    user = get_object_or_404(estudiantes, identificacion=id)
                    status = 'estudiante'
                except:
                    user = None
                
                if user is not None:
                    data = [nombre, primer_apellido, segundo_apellido, status]
                else:
                    status = 'prospecto'
                    data = [nombre, primer_apellido, segundo_apellido, status]
        else:
            data = []
            
    elif len(id) >= 10 and len(id) <= 12:
        data_nombre = data_usuario["nombre"]
        if data_nombre is not None:
            try:
                user = get_object_or_404(profesor, identificacion=id)
                status = 'profesor'
            except:
                user = None
            
            if user is not None:
                
                try:
                    user = get_object_or_404(estudiantes, identificacion=id)
                    status = 'estudianteprofesor'
                except:
                    user = None
                
                if user is not None:
                    data = ['Existe', status]
                else:
                    data = ['Existe', status]    
                    
            else:
                try:
                    user = get_object_or_404(estudiantes, identificacion=id)
                    status = 'estudiante'
                except:
                    user = None
                
                if user is not None:
                    data = ['Existe', status]
                else:
                    status = 'prospecto'
                    data = ['Existe', status]
            
        else:
            try:
                user = get_object_or_404(profesor, identificacion=id)
                status = 'profesor'
            except:
                user = None
            
            if user is not None:
                
                try:
                    user = get_object_or_404(estudiantes, identificacion=id)
                    status = 'estudianteprofesor'
                except:
                    user = None
                
                if user is not None:
                    data = ['',status]
                else:
                    data = ['',status]    
                    
            else:
                try:
                    user = get_object_or_404(estudiantes, identificacion=id)
                    status = 'estudiante'
                except:
                    user = None
                
                if user is not None:
                    data = ['',status]
                else:
                    status = 'prospecto'
                    data = ['',status]
    else:
        data = []
        
        
    data_completa = json.dumps(data)
    return JsonResponse(data_completa, safe=False)


def registrar_accion(usuario, accion):
    registro = RegistroLogsUser(usuario=usuario, accion=accion)
    registro.save()
    


class vistaPerfil (LoginRequiredMixin):
    context_object_name = 'perfil_estudiante'
    template_name = 'Dashboard/Componentes/perfil.html'

    def profile_view(request, id, status):
        user = request.user
        usuario = get_object_or_404(usuarios, auth_user=user.pk)

        if usuario.es_estudiante:

            login = get_object_or_404(estudiantes, identificacion=user.username)

        elif usuario.es_profesor:

            login = get_object_or_404(profesor, identificacion=user.username)

        elif usuario.es_prospecto:

            login = get_object_or_404(prospecto, identificacion=user.username)
   
        try:
            fotoperfil_obj = fotoperfil.objects.get(user=login.user_id) 
            imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))
            context = {
                'user': user,
                'estudiante': login,
                'fotoperfil': imagen_url,
                'status': status,
                'id' : id,
            }
        except fotoperfil.DoesNotExist:

            context = {
                'user': user,
                'estudiante': login,
                'status': status,
                'id' : id,
            }
        return render(request, 'Dashboard/Componentes/perfil.html', context)
    
 
def guardar_perfil(request):
    if request.method == 'POST':
        user = request.user
        numero_telefonico = request.POST.get('numero_telefonico')
        numero_telefonico2 = request.POST.get('numero_telefonico2')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        distrito = request.POST.get('distrito')
        
        user = User.objects.get(username=user.username)
        user_id = user.pk
        
        usuario = get_object_or_404(usuarios, user=user_id)
        
        if usuario.es_profesor or usuario.es_estudiante:
            estudiante = get_object_or_404(estudiantes, identificacion=user.username)
            profesores = get_object_or_404(profesor, identificacion=user.username)
        
            datos_estudiante = [estudiante.identificacion, estudiante.nombre, estudiante.primer_apellido, 
                            estudiante.segundo_apellido, estudiante.fecha_nacimiento, numero_telefonico, numero_telefonico2, estudiante.correo_institucional, estudiante.correo_personal, estudiante.nacionalidad, provincia, canton, distrito, estudiante.sexo]
            
            form = FormularioEstudiantes({ 'identificacion': datos_estudiante[0], 'nombre': datos_estudiante[1], 'primer_apellido': datos_estudiante[2],
                                            'segundo_apellido': datos_estudiante[3], 'fecha_nacimiento': datos_estudiante[4], 'numero_telefonico': datos_estudiante[5], 'numero_telefonico2': datos_estudiante[6],
                                            'correo_institucional': datos_estudiante[7], 'correo_personal': datos_estudiante[8], 'nacionalidad': datos_estudiante[9], 'provincia': datos_estudiante[10], 
                                            'canton': datos_estudiante[11], 'distrito': datos_estudiante[12], 'sexo': datos_estudiante[13]}, instance=estudiante)
            
            if form.is_valid():
                form.save()
                
            datos_profesor = [profesores.identificacion, profesores.nombre, profesores.primer_apellido, 
                            profesores.segundo_apellido, profesores.fecha_nacimiento, numero_telefonico, numero_telefonico2, profesores.correo_institucional, profesores.correo_personal, profesores.nacionalidad, provincia, canton, distrito, profesores.sexo, profesores.puesto_educativo]

            form = FormularioProfesor({ 'identificacion': datos_profesor[0], 'nombre': datos_profesor[1], 'primer_apellido': datos_profesor[2],
                                            'segundo_apellido': datos_profesor[3], 'fecha_nacimiento': datos_profesor[4], 'numero_telefonico': datos_profesor[5], 'numero_telefonico2': datos_profesor[6],
                                            'correo_institucional': datos_profesor[7], 'correo_personal': datos_profesor[8], 'nacionalidad': datos_profesor[9], 'provincia': datos_profesor[10], 
                                            'canton': datos_profesor[11], 'distrito': datos_profesor[12], 'sexo': datos_profesor[13], 'puesto_educativo': datos_profesor[14]}, instance=profesores)
            if form.is_valid():
                form.save()
            
            return redirect(request.META.get('HTTP_REFERER'))
        
        elif usuario.es_profesor or usuario.es_prospecto:
            estudiante = get_object_or_404(prospecto, identificacion=user.username)
            profesores = get_object_or_404(profesor, identificacion=user.username)
            
            datos_profesor = [profesores.identificacion, profesores.nombre, profesores.primer_apellido, 
                            profesores.segundo_apellido, profesores.fecha_nacimiento, numero_telefonico, numero_telefonico2, profesores.correo_institucional, profesores.correo_personal, profesores.nacionalidad, provincia, canton, distrito, profesores.sexo, profesores.puesto_educativo]

            form = FormularioProfesor({ 'identificacion': datos_profesor[0], 'nombre': datos_profesor[1], 'primer_apellido': datos_profesor[2],
                                            'segundo_apellido': datos_profesor[3], 'fecha_nacimiento': datos_profesor[4], 'numero_telefonico': datos_profesor[5], 'numero_telefonico2': datos_profesor[6],
                                            'correo_institucional': datos_profesor[7], 'correo_personal': datos_profesor[8], 'nacionalidad': datos_profesor[9], 'provincia': datos_profesor[10], 
                                            'canton': datos_profesor[11], 'distrito': datos_profesor[12], 'sexo': datos_profesor[13], 'puesto_educativo': datos_profesor[14]}, instance=profesores)
            if form.is_valid():
                form.save()
            
            estudiante = get_object_or_404(prospecto, identificacion=user.username)
            
            datos_estudiante = [estudiante.user, estudiante.identificacion, estudiante.nombre, estudiante.primer_apellido, 
                            estudiante.segundo_apellido, estudiante.fecha_nacimiento, numero_telefonico, numero_telefonico2, estudiante.correo_institucional, 
                            estudiante.correo_personal, estudiante.nacionalidad, provincia, canton, distrito, estudiante.sexo]
            
            form = FormularioProspecto({'user': datos_estudiante[0],'identificacion': datos_estudiante[1], 'nombre': datos_estudiante[2], 'primer_apellido': datos_estudiante[3],
                                            'segundo_apellido': datos_estudiante[4], 'fecha_nacimiento': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6], 'numero_telefonico2': datos_estudiante[7],
                                        'correo_institucional': datos_estudiante[8], 'correo_personal': datos_estudiante[9], 'nacionalidad': datos_estudiante[10], 'provincia': datos_estudiante[11], 
                                        'canton': datos_estudiante[12], 'distrito': datos_estudiante[13], 'sexo': datos_estudiante[14]}, instance=estudiante)

            if form.is_valid():
                form.save()
            
            return redirect(request.META.get('HTTP_REFERER'))
        
        if form.is_valid():
            form.save()
                
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse(status=400) 
    else:
        return HttpResponse(status=400)
    
def mostrar_foto(request):
    user = request.user
    usuario = get_object_or_404(usuarios, auth_user=user.pk)
    foto_perfil = get_object_or_404(fotoperfil, user=usuario.pk)
    foto_bytes = bytes(foto_perfil.archivo)
    return HttpResponse(foto_bytes, content_type='image/png')

lock = threading.Lock()

def enviar_archivo_a_odoo(request):
    if request.method == 'POST':
        user = request.user
        user_id = user.pk
        estudiante = get_object_or_404(usuarios, auth_user=user_id)
        foto = request.FILES.get('fotoperfil')
        
        img_data = foto.read()
        
        # Convertir la imagen a bytes
        img_bytes = bytearray(img_data)

        # Crear el objeto UserFile y guardarlo en la base de datos
        user_file = fotoperfil(user=estudiante, archivo=img_bytes)
        user_file.save()
        
        usuario = get_object_or_404(usuarios, auth_user=user_id)
        formulariodata = [1, 1, False, usuario.pk,'Formulario Enviado Satisfactoriamente']
        
        form = FormularioPrimerIngreso({ 'etapa': formulariodata[0], 'estado': formulariodata[1], 'convalidacion': formulariodata[2],
                                        'usuario': formulariodata[3],'comentario': formulariodata[4]})
        if form.is_valid():
            form.save()
            
        formulariodocumentos = [usuario.pk, True, False, True, True, True, True]
        
        form = FormularioDocumentos({'usuario': formulariodocumentos[0], 'tituloeducacion': formulariodocumentos[1],
                                     'titulouniversitario': formulariodocumentos[2], 'identificacion': formulariodocumentos[3],
                                     'foto': formulariodocumentos[4], 'notas': formulariodocumentos[5],
                                     'plan': formulariodocumentos[6]})
        
        if form.is_valid():
            form.save()
            return redirect('revision_form')
        else:
            return HttpResponse(status=400) 
    else:
        return HttpResponse(status=400)
    
class SessionTimeoutView(LoginRequiredMixin):
    template_name = 'usuarios/login.html'
    login_url = '/login/'
    
    def dispatch(self, request, *args, **kwargs):
        print("Dispatching to session timeout view...")
        logout(request)
        return super().dispatch(request, *args, **kwargs)
    
    
def obtener_provincia(request):
    url = 'https://ubicaciones.paginasweb.cr/provincias.json'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)

def obtener_canton(request):
    id = request.GET.get("provincia_select")
    url = 'https://ubicaciones.paginasweb.cr/provincia/'+id+'/cantones.json'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)

def obtener_distrito(request):
    id_provincia = request.GET.get("provincia_select")
    id_canton = request.GET.get("canton_select")
    url = 'https://ubicaciones.paginasweb.cr/provincia/'+id_provincia+'/canton/'+id_canton+'/distritos.json'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)

def obtener_nacionalidad(request):
    url = 'https://restcountries.com/v3.1/all?fields=name'
    response = requests.get(url)
    data = response.json()
    countries = []
    for country in data:
        countries.append(country["name"]["common"])
    return JsonResponse(sorted(countries), safe=False)

class DashboardEstudianteView(LoginRequiredMixin, View):
    login_url = ''  # Ruta de inicio de sesión
    redirect_field_name = 'login'  # Nombre del campo de redirección

    def get(self, request, id, status):
        return render(request, 'Dashboard/dashboard.html', {'id': id, 'status': status})
    
class DashboardProfesorView(LoginRequiredMixin, View):
    login_url = ''  # Ruta de inicio de sesión
    redirect_field_name = 'login'  # Nombre del campo de redirección

    def get(self, request, id, status):
        return render(request, 'Dashboard/dashboard.html', {'id': id, 'status': status})
    
def sesion_expirada(request):
    return render(request, 'sesion_expirada.html') 

def change_email(request):
    codigo = random.randint(100000, 999999)
    
    user = request.user
    subject = 'Cambio de Correo Electronico'
    message = f'Hola, {user.username}, se ha solicitado modificar el correo electronico personal.\n\nEl código es: {codigo}\n\nEL CODIGO SOLO ES VALIDO PARA EL DIA DE HOY.\n\nUn cordial saludo.\nUIA.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    
    send_mail( subject, message, email_from, recipient_list )
    
    return render(request, 'usuario/cambio_correo_codigo.html', {'codigo': codigo})

def change_email_correct(request):
    if request.method == 'POST':
        user = request.user
        
        nuevo_correo = request.POST.get('nuevo_correo2')
        
        user = User.objects.get(username=user.username)
        user_id = user.pk
        
        estudiante = get_object_or_404(prospecto, identificacion=user.username)
            
        datos_estudiante = [estudiante.user, estudiante.identificacion, estudiante.nombre, estudiante.primer_apellido, 
                        estudiante.segundo_apellido, estudiante.fecha_nacimiento, estudiante.numero_telefonico, estudiante.numero_telefonico2, estudiante.correo_institucional, 
                        nuevo_correo, estudiante.nacionalidad, estudiante.provincia, estudiante.canton, estudiante.distrito, estudiante.sexo]
        
        form = FormularioProspecto({'user': datos_estudiante[0],'identificacion': datos_estudiante[1], 'nombre': datos_estudiante[2], 'primer_apellido': datos_estudiante[3],
                                        'segundo_apellido': datos_estudiante[4], 'fecha_nacimiento': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6], 'numero_telefonico2': datos_estudiante[7],
                                        'correo_institucional': datos_estudiante[8], 'correo_personal': datos_estudiante[9], 'nacionalidad': datos_estudiante[10], 'provincia': datos_estudiante[11], 
                                        'canton': datos_estudiante[12], 'distrito': datos_estudiante[13], 'sexo': datos_estudiante[14]}, instance=estudiante)
    
        if form.is_valid():
            form.save()
            return redirect('perfil_prospecto')
        
def revision_formulario(request):
    user = request.user
    user_id = user.pk 
    usuario = get_object_or_404(usuarios, auth_user=user_id)
    
    # Obtener el objeto de la base de datos según su ID
    statusgeneral = get_object_or_404(primerIngreso, usuario=usuario.pk)
    
    etapa  = get_object_or_404(etapas, id_etapa=statusgeneral.etapa_id)
    
    estado = get_object_or_404(estados, id_estado=statusgeneral.estado_id)
    
    docs = get_object_or_404(documentos, usuario=usuario.pk)

    # Enviar el objeto y otros datos necesarios a la plantilla HTML
    contexto = {
        "comentario": statusgeneral.comentario,
        "etapa": etapa.etapa_nombre,
        "estado": estado.estado_nombre,
        "convalidacion" : statusgeneral.convalidacion,
        "documentos": docs,
    }
    return render(request, "Prospecto/revision_form.html", contexto)

def corregirdata(request):
    user = request.user
    user_id = user.pk
    
    datocargado = request.POST.get('documentocargado')
    
    usuario = get_object_or_404(usuarios, auth_user=user_id)
    
    statusgeneral = get_object_or_404(primerIngreso, usuario=usuario.pk)
    docs = get_object_or_404(documentos, usuario=usuario.pk)
    
    formulariodata = [2, 3, False, usuario.pk, statusgeneral.comentario]
        
    form = FormularioPrimerIngreso({ 'etapa': formulariodata[0], 'estado': formulariodata[1], 'convalidacion': formulariodata[2],
                                        'usuario': formulariodata[3],'comentario': formulariodata[4]}, instance=statusgeneral)
    if form.is_valid():
        form.save()
        
    if datocargado == "titulo":
        formulariodocs = [usuario.pk, True, docs.titulouniversitario, 
                          docs.identificacion, docs.foto, docs.notas, docs.plan]
    elif datocargado == "titulouniversitario":
        formulariodocs = [usuario.pk, docs.tituloeducacion, True, 
                          docs.identificacion, docs.foto, docs.notas, docs.plan]
    elif datocargado == "identificacion":
        formulariodocs = [usuario.pk, docs.tituloeducacion, docs.titulouniversitario, 
                          True, docs.foto, docs.notas, docs.plan]
    elif datocargado == "foto":
        formulariodocs = [usuario.pk, docs.tituloeducacion, docs.titulouniversitario, 
                          docs.identificacion, True, docs.notas, docs.plan]
    elif datocargado == "notas":
        formulariodocs = [usuario.pk, docs.tituloeducacion, docs.titulouniversitario, 
                          docs.identificacion, docs.foto, True, docs.plan]
    elif datocargado == "plan":
        formulariodocs = [usuario.pk, docs.tituloeducacion, docs.titulouniversitario, 
                          docs.identificacion, docs.foto, docs.notas, True]
        
    form = FormularioDocumentos({'usuario': formulariodocs[0], 'tituloeducacion': formulariodocs[1],
                                     'titulouniversitario': formulariodocs[2], 'identificacion': formulariodocs[3],
                                     'foto': formulariodocs[4], 'notas': formulariodocs[5],
                                     'plan': formulariodocs[6]}, instance=docs)
        
    if form.is_valid():
        form.save()
        return redirect(request.META.get('HTTP_REFERER'))
