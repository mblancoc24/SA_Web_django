from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import FormularioEstudiantes, FormularioUsuario, FormularioProfesor
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import usuarios, profesor, estudiantes, RegistroLogsUser
import requests
import json
import django
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password

class Logueo(LoginView):
    template_name = 'usuario/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        username = self.request.POST.get('username')
        user = User.objects.get(username=username)
        user_id = user.pk
        
        login = get_object_or_404(usuarios, id=user_id)
        
        login = get_object_or_404(usuarios, id=user_id)
        
        if login.es_estudiante and login.es_profesor:
            return HttpResponse('login.html', {'mostrar_modal': True})
        else:
            if login.es_prospecto:
                return reverse_lazy('usuario_prospecto')
            
            elif login.es_estudiante:
                return reverse_lazy('usuario_estudiante')
            
            elif login.es_profesor:
                return reverse_lazy('usuario_profesor')



class PaginaRegistroEstudiante(FormView):
    template_name = 'usuario/registro_estudiantes.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('usuario_estudiante')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        nombre_estudiante = self.request.POST.get('nombre')
        primerapellido = self.request.POST.get('primerapellido')
        segundoapellido = self.request.POST.get('segundoapellido')
        fecha = self.request.POST.get('fechanacimiento')
        telefono = self.request.POST.get('telefono')
        correo = self.request.POST.get('correo')

        Usuarios = form.save()
        
        user = User.objects.get(username=username)
        user_id = user.pk
        
        datos_usuario = [user_id, False, False, False, True, user_id]
        
        form = FormularioUsuario({'usuarios': datos_usuario[0],  'activo': datos_usuario[1], 'es_profesor': datos_usuario[2], 'es_estudiante': datos_usuario[3], 'es_prospecto': datos_usuario[4]})
        
        if form.is_valid():
            form.save()
        
        id_usuario = get_object_or_404(usuarios, id=user_id)
        
        datos_estudiante = [id_usuario, username, nombre_estudiante, primerapellido, 
                            segundoapellido, fecha, telefono, correo]
        
        form = FormularioEstudiantes({ 'user': datos_estudiante[0], 'identificacion': datos_estudiante[1], 'nombre': datos_estudiante[2], 'primer_apellido': datos_estudiante[3],
                                      'segundo_apellido': datos_estudiante[4], 'fecha_nacimiento': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6],
                                      'correo': datos_estudiante[7]})
        if form.is_valid():
            form.save()
            
        if Usuarios is not None:
            login(self.request, Usuarios)
            registrar_accion(self.request.user, 'El usuario '+ username +' se ha creado una cuenta como prospecto.')
        return super(PaginaRegistroEstudiante, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('usuario_estudiante')
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

def modalusuario(request):
    return render (request, 'modal.html')