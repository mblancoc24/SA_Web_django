from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
import os
from django.utils import timezone
from django.contrib.auth import login, update_session_auth_hash
from .forms import FormularioEstudiantes, FormularioUsuario, FormularioProfesor, FormularioInfoEstudiante, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import FormularioEstudiantes, FormularioUsuario, FormularioProfesor
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import usuarios, profesor, estudiantes, RegistroLogsUser, carreras, colegios, posgrados, fotoperfil
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import requests
import json
import django
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.apps import AppConfig
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from django.contrib import messages
from django.core.files import File
from django.core.files.base import ContentFile
from PIL import Image
from odoorpc import ODOO
import base64
import threading
import xmlrpc.client

from django.http import HttpResponse

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
        login_obj = get_object_or_404(usuarios, usuarios=user.id)
        if login_obj.es_estudiante and login_obj.es_profesor:
            primer_ingreso = user.password
            #ACA SE CONSULTARIA A LA BASE DE DATOS DE LAS CLAVES PREDETERMINADAS
            if primer_ingreso == 'admin1818':
                registrar_accion(self.request.user, 'El usuario {0} ha realizado un cambio de contrasena y ha ingresado.'.format(username))
                modal = True
                return render(self.request, 'login.html', {'modal': modal})
            else:
                registrar_accion(self.request.user, 'El usuario {0} ha ingresado como profesor.'.format(username))
                modal = True
                return render(self.request, 'login.html', {'modal': modal})
        else:
            if login_obj.es_prospecto:
                registrar_accion(self.request.user, 'El usuario {0} ha ingresado como prospecto.'.format(username))
                return redirect('usuario_prospecto')
            
            elif login_obj.es_estudiante:
                registrar_accion(self.request.user, 'El usuario {0} ha ingresado como estudiante.'.format(username))
                return redirect('usuario_estudiante')
            
            elif login_obj.es_profesor:
                registrar_accion(self.request.user, 'El usuario {0} ha ingresado como profesor.'.format(username))
                #ACA SE CONSULTARIA A LA BASE DE DATOS DE LAS CLAVES PREDETERMINADAS
                primer_ingreso = self.request.POST.get('password')
                if primer_ingreso == 'admin1818':
                    registrar_accion(self.request.user, 'El usuario {0} ha realizado un cambio de contrasena  y ha ingresado.'.format(username))
                    return redirect('cambiar_contrasena')
                else:
                    return redirect('usuario_profesor')

class cambiarcontrasena (LoginRequiredMixin):
    def cambiar_contrasena(request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                login_obj = get_object_or_404(usuarios, usuarios=user.id)
                if login_obj.es_prospecto:
                    return redirect('usuario_prospecto')
                    
                elif login_obj.es_estudiante:
                    return redirect('usuario_estudiante')
                    
                elif login_obj.es_profesor:
                    return redirect('usuario_profesor')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'Contrasenas/Correo/cambiar_contrasena.html', {'form': form})

class PaginaRegistroEstudiante(FormView):
    template_name = 'usuario/registro_estudiantes.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('usuario_prospecto')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        nombre_estudiante = self.request.POST.get('nombre')
        primerapellido = self.request.POST.get('primerapellido')
        segundoapellido = self.request.POST.get('segundoapellido')
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
        
        form = FormularioUsuario({'usuarios': datos_usuario[0],  'activo': datos_usuario[1], 'es_profesor': datos_usuario[2], 'es_estudiante': datos_usuario[3], 'es_prospecto': datos_usuario[4], 'es_cursolibre': datos_usuario[5]})
        
        if form.is_valid():
            form.save()
        
        usuario = get_object_or_404(usuarios, usuarios=user_id)
        id_usuario = usuario.usuarios_id
        
        datos_estudiante = [id_usuario, username, nombre_estudiante, primerapellido, 
                            segundoapellido, fecha, telefono, 'No Asignado', correo_personal, nacionalidad, provincia, canton, distrito, sexo]
        
        form = FormularioEstudiantes({ 'user': datos_estudiante[0], 'identificacion': datos_estudiante[1], 'nombre': datos_estudiante[2], 'primer_apellido': datos_estudiante[3],
                                      'segundo_apellido': datos_estudiante[4], 'fecha_nacimiento': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6],
                                      'correo_institucional': datos_estudiante[7], 'correo_personal': datos_estudiante[8], 'nacionalidad': datos_estudiante[9], 'provincia': datos_estudiante[10], 
                                      'canton': datos_estudiante[11], 'distrito': datos_estudiante[12], 'sexo': datos_estudiante[13]})
        if form.is_valid():
            form.save()
            
        if Usuarios is not None:
            login(self.request, Usuarios)
            registrar_accion(self.request.user, 'El usuario '+ username +' se ha creado una cuenta como prospecto.')
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
    identificiacion = request.GET.get("identificacion")
    url = 'https://api.hacienda.go.cr/fe/ae?identificacion=' + identificiacion
    response = requests.get(url)
    
    data_usuario = json.loads(response.text)
        
    if len(identificiacion) == 9:
        data_nombre = data_usuario["nombre"]
        if data_nombre is not None:
            nombre_completo = data_nombre.split()
            
            nombre = ' '.join(nombre_completo[:-2]).title()
            primer_apellido = nombre_completo[-2].title()
            segundo_apellido = nombre_completo[-1].title()
            data = [nombre, primer_apellido, segundo_apellido]
        else:
            data = []
            
    elif len(identificiacion) >= 10 and len(identificiacion) <= 12:
        data_nombre = data_usuario["nombre"]
        if data_nombre is not None:
            data = ['Existe']
        else:
            data = []
    else:
        data = []
        
        
    data_completa = json.dumps(data)
    return JsonResponse(data_completa, safe=False)

class MyPasswordResetView(PasswordResetView):
    template_name = 'Contrasenas/Correo/my_password_reset.html'
    email_template_name = 'Contrasenas/Correo/my_password_reset_email.html'
    subject_template_name = 'Contrasenas/Correo/my_password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    from_email = 'correouianoreply@gmail.com'
    
class MyPasswordReset(FormView):
    template_name = 'Contrasenas/Correo/my_password_reset.html'
    success_url = reverse_lazy('password_reset_email')
    

        
    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user is not None:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = self.request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
            full_reset_url = f"{settings.PROTOCOL}://{settings.DOMAIN_NAME}{reset_url}"
            send_mail(
                'Restablecer contraseña',
                'Por favor, sigue este enlace para restablecer tu contraseña: {}'.format(full_reset_url),
                self.from_email,
                [email],
                fail_silently=False,
                html_message='Haz clic <a href="{}">aquí</a> para restablecer tu contraseña.'.format(full_reset_url)
            )
        return super().form_valid(form)
    
class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'Contrasenas/Correo/my_password_reset_done.html'
    success_url = reverse_lazy('password_reset_done')


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
            fotoperfiles = fotoperfil.objects.get(user=estudiante.user_id)
            imagen_url = Image.open(ContentFile(fotoperfiles.archivo))
            context = {'user': user,
                'estudiante':estudiante,
                'fotoperfil':imagen_url}
        except fotoperfil.DoesNotExist:
            fotoperfiles = None
            context = {'user': user,
                'estudiante':estudiante,
                'fotoperfil':'../static/img/user.png'}
            
        return render(request, 'Prospecto/perfil.html', context)
    
 
def guardar_perfil(request):
    if request.method == 'POST':
        user = request.user
        numero_telefonico = request.POST.get('numero_telefonico')
        correo_personal = request.POST.get('correo_personal')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        distrito = request.POST.get('distrito')
        
        user = User.objects.get(username=user.username)
        user_id = user.pk
        
        estudiante = get_object_or_404(estudiantes, user=user_id)
        
        datos_estudiante = [estudiante.id_estudiante, estudiante.identificacion, estudiante.nombre, estudiante.primer_apellido, 
                        estudiante.segundo_apellido, estudiante.fecha_nacimiento, numero_telefonico, estudiante.correo_institucional, correo_personal, estudiante.nacionalidad, provincia, canton, distrito, estudiante.sexo]
        
        form = FormularioEstudiantes({ 'user': datos_estudiante[0], 'identificacion': datos_estudiante[1], 'nombre': datos_estudiante[2], 'primer_apellido': datos_estudiante[3],
                                        'segundo_apellido': datos_estudiante[4], 'fecha_nacimiento': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6],
                                        'correo_institucional': datos_estudiante[7], 'correo_personal': datos_estudiante[8], 'nacionalidad': datos_estudiante[9], 
                                        'provincia': datos_estudiante[10], 'canton': datos_estudiante[11], 'distrito': datos_estudiante[12], 'sexo': datos_estudiante[13]}, instance=estudiante)
        

        if form.is_valid():
            form.save()
            return redirect('usuario_prospecto')
        else:
            return HttpResponse(status=400) 
    else:
        return HttpResponse(status=400)
    
def mostrar_foto(request):
    user = request.user
    usuario = get_object_or_404(usuarios, usuarios=user.pk)
    estudiante = get_object_or_404(estudiantes, user=usuario.usuarios_id)
    foto_perfil = get_object_or_404(fotoperfil, user=estudiante.user_id)
    foto_bytes = bytes(foto_perfil.archivo)
    return HttpResponse(foto_bytes, content_type='image/png')

lock = threading.Lock()

def enviar_archivo_a_odoo(request):
    if request.method == 'POST':
        user = request.user
        user_id = user.pk
        estudiante = get_object_or_404(estudiantes, user=user_id)
        foto = request.FILES.get('fotoperfil')
        
        img_data = foto.read()
        
        # Convertir la imagen a bytes
        img_bytes = bytearray(img_data)

        # Crear el objeto UserFile y guardarlo en la base de datos
        user_file = fotoperfil(user=estudiante.user_id, archivo=img_bytes)
        user_file.save()
    
    return redirect('usuario_prospecto')

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