from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, update_session_auth_hash
from .forms import FormularioEstudiantes, FormularioUsuario, FormularioProfesor, FormularioInfoEstudiante, CustomUserCreationForm

from django.contrib.auth import login, authenticate
from .forms import FormularioEstudiantes, FormularioUsuario, FormularioProfesor

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import usuarios, profesor, estudiantes, RegistroLogsUser, carreras, colegios, posgrados
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

from django.contrib import messages

class Logueo(LoginView):
    template_name = 'usuario/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        # Get the user object from the form data
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        
        # Call the parent form_valid method if the user is not authenticated
        if user is None:
            form.add_error('username', 'El usuario no existe en el sistema')
            return super().form_invalid(form)
        
        # Authenticate the user and log them in
        login(self.request, user)
        login_obj = get_object_or_404(usuarios, id=user.id)
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
    # def form_invalid(self, form):
    # # Add an error message to the context
    #     error = 'El usuario o la contraseña son incorrectos.'
    #     return render(self.request, 'login.html', {'form': form, 'error': error})

class cambiarcontrasena (LoginRequiredMixin):
    def cambiar_contrasena(request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                login_obj = get_object_or_404(usuarios, id=user.id)
                if login_obj.es_prospecto:
                    return redirect('usuario_prospecto')
                    
                elif login_obj.es_estudiante:
                    return redirect('usuario_estudiante')
                    
                elif login_obj.es_profesor:
                    return redirect('usuario_profesor')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'cambiar_contrasena.html', {'form': form})

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
        direccion = self.request.POST.get('direccion')

        Usuarios = form.save() # type: ignore
        
        user = User.objects.get(username=username)
        user_id = user.pk
        
        datos_usuario = [user_id, False, False, False, True, False]
        
        form = FormularioUsuario({'usuarios': datos_usuario[0],  'activo': datos_usuario[1], 'es_profesor': datos_usuario[2], 'es_estudiante': datos_usuario[3], 'es_prospecto': datos_usuario[4], 'es_cursolibre': datos_usuario[5]})
        
        if form.is_valid():
            form.save()
        
        id_usuario = get_object_or_404(usuarios, id=user_id)
        
        datos_estudiante = [id_usuario, username, nombre_estudiante, primerapellido, 
                            segundoapellido, fecha, telefono, 'No Asignado', correo_personal, direccion]
        
        form = FormularioEstudiantes({ 'user': datos_estudiante[0], 'identificacion': datos_estudiante[1], 'nombre': datos_estudiante[2], 'primer_apellido': datos_estudiante[3],
                                      'segundo_apellido': datos_estudiante[4], 'fecha_nacimiento': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6],
                                      'correo_institucional': datos_estudiante[7], 'correo_personal': datos_estudiante[8], 'direccion': datos_estudiante[9]})
        if form.is_valid():
            form.save()
            
        if Usuarios is not None:
            login(self.request, Usuarios)
            registrar_accion(self.request.user, 'El usuario '+ username +' se ha creado una cuenta como prospecto.')
        return super(PaginaRegistroEstudiante, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('usuario_prospecto')
        return super(PaginaRegistroEstudiante, self).get(*args, **kwargs)


class DetalleUsuarioEstudiante(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'prueba_estudiante'
    template_name = 'usuario/prueba_estudiante.html'
    
class DetalleUsuarioProfesor(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'prueba_profesor'
    template_name = 'usuario/prueba_profesor.html'
    
class DetalleUsuarioProspecto(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'prueba_prospecto'
    template_name = 'usuario/prueba_prospecto.html'
    
class DetalleUsuarioEstudianteProfesor(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'opciones_estudiante_profesor'
    template_name = 'usuario/opciones_login.html'

class CrearUsuario(LoginRequiredMixin, CreateView):
    model = usuarios
    fields = ['nombre', 'primer_apellido', 'segundo_apellido','segundo_apellido']
    success_url = reverse_lazy('usuario')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearUsuario, self).form_valid(form)

def obtener_datos(request):
    print(django.get_version())
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
    template_name = 'my_password_reset.html'
    email_template_name = 'my_password_reset_email.html'
    subject_template_name = 'my_password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    from_email = 'correouianoreply@gmail.com'

    def form_valid(self, form):
        # Agregamos el código para enviar el correo electrónico personalizado aquí
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user is not None:
            send_mail(
                'Restablecer contraseña',
                'Por favor, sigue este enlace para restablecer tu contraseña:',
                self.from_email,
                [email],
                fail_silently=False,
                html_message='Haz clic <a href="{}">aquí</a> para restablecer tu contraseña.'.format(self.get_success_url())
            )
        return super().form_valid(form)
    
class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'my_password_reset_done.html'
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
    valores = colegios.objects.values_list('nombre_carrera', flat=True)
    return JsonResponse(list(valores), safe=False)

class vistaPerfil (LoginRequiredMixin):
    context_object_name = 'perfil_estudiante'
    template_name = 'usuario/perfil.html'


    def profile_view(request):
        user = request.user
        usuario = get_object_or_404(usuarios, id=user.pk)
        estudiante = get_object_or_404(estudiantes, user=usuario.id)
        context = {'user': user,
                'estudiante':estudiante}
        return render(request, 'perfil.html', context)
    
    def form_valid(self, form):
        
        numero_telefonico = self.request.POST.get('numero_telefonico')
        correo_personal = self.request.POST.get('correo_personal')
        
        data = [numero_telefonico, correo_personal]
        return super(vistaPerfil, self).form_valid(form)
