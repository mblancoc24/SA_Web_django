from django.shortcuts import render, redirect, get_object_or_404
from .models import usuarios, profesor, estudiantes, RegistroLogsUser, carreras, colegios, posgrados, fotoperfil, estados, etapas, primerIngreso
from .forms import FormularioEstudiantes, FormularioUsuario, FormularioPrimerIngreso, FormularioProfesor, FormularioProspecto, FormularioInfoEstudiante, CustomUserCreationForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.decorators import login_required
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
                modal = True
                return render(self.request, 'usuario/login.html', {'modal': modal})
            
        elif login_obj.es_prospecto and login_obj.es_profesor:
            #ACA SE CONSULTARIA A LA BASE DE DATOS DE LAS CLAVES PREDETERMINADAS
            if password == 'Admin1818$':
                registrar_accion(login_obj, 'El usuario {0} ha realizado un cambio de contrasena y ha ingresado.'.format(username))
                modal = True
                return redirect('change_password')
            else:
                registrar_accion(login_obj, 'El usuario {0} ha ingresado como profesor.'.format(username))
                modal = True
                return render(self.request, 'usuario/login.html', {'modal': modal})
        else:
            if login_obj.es_prospecto:
                registrar_accion(login_obj, 'El usuario {0} ha ingresado como prospecto.'.format(username))
                return redirect('usuario_prospecto')
            
            elif login_obj.es_estudiante:
                registrar_accion(login_obj, 'El usuario {0} ha ingresado como estudiante.'.format(username))
                return redirect('usuario_estudiante')
            
            elif login_obj.es_profesor:
                registrar_accion(login_obj, 'El usuario {0} ha ingresado como profesor.'.format(username))
                #ACA SE CONSULTARIA A LA BASE DE DATOS DE LAS CLAVES PREDETERMINADAS
                if password == 'Admin1818$':
                    registrar_accion(self.request.user, 'El usuario {0} ha realizado un cambio de contrasena  y ha ingresado.'.format(username))
                    return redirect('change_password')
                else:
                    return redirect('usuario_profesor')


class PaginaRegistroEstudiante(FormView):
    template_name = 'usuario/registro_estudiantes.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('usuario_prospecto')

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
                                profesor_usuario.segundo_apellido, profesor_usuario.fecha_nacimiento, profesor_usuario.numero_telefonico, profesor_usuario.correo_institucional, 
                                profesor_usuario.correo_personal, profesor_usuario.nacionalidad, profesor_usuario.provincia, profesor_usuario.canton, profesor_usuario.distrito, profesor_usuario.sexo]
            
            form = FormularioEstudiantes({'identificacion': datos_estudiante[0], 'nombre': datos_estudiante[1], 'primer_apellido': datos_estudiante[2],
                                        'segundo_apellido': datos_estudiante[3], 'fecha_nacimiento': datos_estudiante[4], 'numero_telefonico': datos_estudiante[5],
                                        'correo_institucional': datos_estudiante[6], 'correo_personal': datos_estudiante[7], 'nacionalidad': datos_estudiante[8], 'provincia': datos_estudiante[9], 
                                        'canton': datos_estudiante[10], 'distrito': datos_estudiante[11], 'sexo': datos_estudiante[12]})
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
                                segundoapellido, fecha, telefono, 'No Asignado', correo_personal, nacionalidad, provincia, canton, distrito, sexo]
            
            form = FormularioProspecto({'user': datos_estudiante[0],'identificacion': datos_estudiante[1], 'nombre': datos_estudiante[2], 'primer_apellido': datos_estudiante[3],
                                        'segundo_apellido': datos_estudiante[4], 'fecha_nacimiento': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6],
                                        'correo_institucional': datos_estudiante[7], 'correo_personal': datos_estudiante[8], 'nacionalidad': datos_estudiante[9], 'provincia': datos_estudiante[10], 
                                        'canton': datos_estudiante[11], 'distrito': datos_estudiante[12], 'sexo': datos_estudiante[13]})
            if form.is_valid():
                form.save()
            
        if Usuarios is not None:
            user = get_object_or_404(usuarios, auth_user=user_id)
            login(self.request, Usuarios)
            registrar_accion(user, 'El usuario '+ username +' se ha creado una cuenta como prospecto.')
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
    template_name = 'Prospecto/prueba_prospecto.html'
    
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
    
def carrerasselect(request):
    valores = carreras.objects.values_list('nombre_carrera', flat=True)
    return JsonResponse(list(valores), safe=False)

def colegiosselect(request):
    valores = colegios.objects.values_list('nombre_colegio', flat=True)
    return JsonResponse(list(valores), safe=False)

def posgradosselect(request):
    valores = posgrados.objects.values_list('nombre_carrera', flat=True)
    return JsonResponse(list(valores), safe=False)

class vistaPerfil (LoginRequiredMixin):
    context_object_name = 'perfil_estudiante'
    template_name = 'Prospecto/perfil.html'

    def profile_view(request):
        user = request.user
        usuario = get_object_or_404(usuarios, usuarios=user.pk)
        estudiante = get_object_or_404(estudiantes, user=usuario.usuarios_id)
   
        try:
            fotoperfil_obj = fotoperfil.objects.get(user=estudiante.user_id) 
            imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))
            context = {
                'user': user,
                'estudiante': estudiante,
                'fotoperfil': imagen_url,
            }
        except fotoperfil.DoesNotExist:

            context = {
                'user': user,
                'estudiante': estudiante,
            }
        return render(request, 'Prospecto/perfil.html', context)
    
 
def guardar_perfil(request):
    if request.method == 'POST':
        user = request.user
        numero_telefonico = request.POST.get('numero_telefonico')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        distrito = request.POST.get('distrito')
        
        user = User.objects.get(username=user.username)
        user_id = user.pk
        
        estudiante = get_object_or_404(estudiantes, user=user_id)
        
        datos_estudiante = [estudiante.id_estudiante, estudiante.identificacion, estudiante.nombre, estudiante.primer_apellido, 
                        estudiante.segundo_apellido, estudiante.fecha_nacimiento, numero_telefonico, estudiante.correo_institucional, estudiante.correo_personal, estudiante.nacionalidad, provincia, canton, distrito, estudiante.sexo]
        
        form = FormularioEstudiantes({ 'identificacion': datos_estudiante[0], 'nombre': datos_estudiante[1], 'primer_apellido': datos_estudiante[2],
                                        'segundo_apellido': datos_estudiante[3], 'fecha_nacimiento': datos_estudiante[4], 'numero_telefonico': datos_estudiante[5],
                                        'correo_institucional': datos_estudiante[6], 'correo_personal': datos_estudiante[7], 'nacionalidad': datos_estudiante[8], 'provincia': datos_estudiante[9], 
                                        'canton': datos_estudiante[10], 'distrito': datos_estudiante[11], 'sexo': datos_estudiante[12]}, instance=estudiante)
        

        if form.is_valid():
            form.save()
            return redirect('usuario_prospecto')
        else:
            return HttpResponse(status=400) 
    else:
        return HttpResponse(status=400)
    
def mostrar_foto(request):
    user = request.user
    usuario = get_object_or_404(usuarios, auth_user=user.pk)
    estudiante = get_object_or_404(estudiantes, user=usuario.usuarios_id)
    foto_perfil = get_object_or_404(fotoperfil, user=estudiante.user_id)
    foto_bytes = bytes(foto_perfil.archivo)
    return HttpResponse(foto_bytes, content_type='image/png')

lock = threading.Lock()

def enviar_archivo_a_odoo(request):
    if request.method == 'POST':
        user = request.user
        user_id = user.pk
        # estudiante = get_object_or_404(usuarios, auth_user=user_id)
        # foto = request.FILES.get('fotoperfil')
        
        # img_data = foto.read()
        
        # # Convertir la imagen a bytes
        # img_bytes = bytearray(img_data)

        # # Crear el objeto UserFile y guardarlo en la base de datos
        # user_file = fotoperfil(user=estudiante.user_id, archivo=img_bytes)
        # user_file.save()
        
        usuario = get_object_or_404(usuarios, auth_user=user_id)
        formulariodata = [1, 1, usuario.pk,'Formulario Enviado Satisfactoriamente']
        
        form = FormularioPrimerIngreso({ 'etapa': formulariodata[0], 'estado': formulariodata[1],
                                        'usuario': formulariodata[2],'comentario': formulariodata[3]})
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

    def get(self, request, id):
        return render(request, 'Dashboard/Estudiante/estudiante.html', {'id': id})
    
class DashboardProfesorView(LoginRequiredMixin, View):
    login_url = ''  # Ruta de inicio de sesión
    redirect_field_name = 'login'  # Nombre del campo de redirección

    def get(self, request, id):
        return render(request, 'Dashboard/Profesor/profesor.html', {'id': id})
    
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
        
        estudiante = get_object_or_404(estudiantes, user=user_id)
        
        datos_estudiante = [estudiante.id_estudiante, estudiante.identificacion, estudiante.nombre, estudiante.primer_apellido, 
                        estudiante.segundo_apellido, estudiante.fecha_nacimiento, estudiante.numero_telefonico, estudiante.correo_institucional, 
                        nuevo_correo, estudiante.nacionalidad, estudiante.provincia, estudiante.canton, estudiante.distrito, estudiante.sexo]
        
        form = FormularioEstudiantes({ 'identificacion': datos_estudiante[0], 'nombre': datos_estudiante[1], 'primer_apellido': datos_estudiante[2],
                                        'segundo_apellido': datos_estudiante[3], 'fecha_nacimiento': datos_estudiante[4], 'numero_telefonico': datos_estudiante[5],
                                        'correo_institucional': datos_estudiante[6], 'correo_personal': datos_estudiante[7], 'nacionalidad': datos_estudiante[8], 'provincia': datos_estudiante[9], 
                                        'canton': datos_estudiante[10], 'distrito': datos_estudiante[11], 'sexo': datos_estudiante[12]}, instance=estudiante)
    
        if form.is_valid():
            form.save()
            return render(request, 'Prospecto/perfil.html')
        
def revision_formulario(request):
    user = request.user
    user_id = user.pk 
    usuario = get_object_or_404(usuarios, auth_user=user_id)
    
    # Obtener el objeto de la base de datos según su ID
    statusgeneral = get_object_or_404(primerIngreso, usuario=usuario.pk)
    
    etapa  = get_object_or_404(etapas, id_etapa=statusgeneral.etapa_id)
    
    estado = get_object_or_404(estados, id_estado=statusgeneral.estado_id)

    # Enviar el objeto y otros datos necesarios a la plantilla HTML
    contexto = {
        "comentario": statusgeneral.comentario,
        "etapa": etapa.etapa_nombre,
        "estado": estado.estado_nombre,
    }
    return render(request, "Prospecto/revision_form.html", contexto)