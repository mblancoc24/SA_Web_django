from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import FormularioEstudiantes, FormularioUsuario, FormularioProfesor
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import usuarios, profesor, estudiantes
import requests
import json
import django
from django.http import JsonResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

class Logueo(LoginView):
    template_name = 'usuario/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        username = self.request.POST.get('username')
        user = User.objects.get(username=username)
        user_id = user.pk
        
        login = get_object_or_404(usuarios, id=user_id)
        
        if login.Tipo == '1':
            return reverse_lazy('usuario_profesor')
        
        elif login.Tipo == '2':
            return reverse_lazy('usuario_estudiante')


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
        
        datos_usuario = ['2', True, user_id]
        
        form = FormularioUsuario({'Tipo': datos_usuario[0], 'estado': datos_usuario[1], 'usuarios': datos_usuario[2]})
        
        if form.is_valid():
            form.save()
        
        id_usuario = get_object_or_404(usuarios, id=user_id)
        
        datos_estudiante = [username, nombre_estudiante, primerapellido, 
                            segundoapellido, fecha, telefono, correo, False, False, id_usuario]
        
        form = FormularioEstudiantes({'Cedula': datos_estudiante[0], 'nombre': datos_estudiante[1], 'primer_apellido': datos_estudiante[2],
                                      'segundo_apellido': datos_estudiante[3], 'fecha_nacimiento': datos_estudiante[4], 'phone_tutor': datos_estudiante[5],
                                      'correo_estudiante': datos_estudiante[6], 'pago_realizado': datos_estudiante[7],
                                      'documentos_presentados': datos_estudiante[8], 'user': datos_estudiante[9]})
        if form.is_valid():
            form.save()
            
        if Usuarios is not None:
            login(self.request, Usuarios)
        return super(PaginaRegistroEstudiante, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('usuario_estudiante')
        return super(PaginaRegistroEstudiante, self).get(*args, **kwargs)

# class PaginaRegistroProfesor(FormView):
#     template_name = 'usuario/registro_profesor.html'
#     form_class = UserCreationForm
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('usuario_profesor')
    

#     def form_valid(self, form):
#         username = form.cleaned_data['username']
#         password_profesor = form.cleaned_data['password2']
#         nombre_profesor = self.request.POST.get('nombre')
#         primerapellido = self.request.POST.get('primerapellido')
#         segundoapellido = self.request.POST.get('segundoapellido')
#         puestoeducativo = self.request.POST.get('puestoeducativo')
#         correo = self.request.POST.get('correo')
        
#         Usuarios = form.save() # type: ignore
        
#         user = User.objects.get(username=username)
#         user_id = user.pk
        
#         datos_usuario = ['1', True, user_id]
        
#         form = FormularioUsuario({'Tipo': datos_usuario[0], 'estado': datos_usuario[1], 'usuarios': datos_usuario[2]})
        
#         if form.is_valid():
#             form.save()
        
#         id_usuario = get_object_or_404(usuarios, id=user_id)
        
#         datos_profesor = [username, nombre_profesor, primerapellido, 
#                             segundoapellido, correo, puestoeducativo, password_profesor, id_usuario]
        
#         form = FormularioProfesor({'Cedula': datos_profesor[0], 'nombre': datos_profesor[1], 'primer_apellido': datos_profesor[2],
#                                 'segundo_apellido': datos_profesor[3], 'correo_profesor': datos_profesor[4], 'puesto_educativo': datos_profesor[5],
#                                 'password': datos_profesor[6], 'user': datos_profesor[7]})
        
#         if form.is_valid():
#             form.save()
            
#         if Usuarios is not None:
#             login(self.request, Usuarios)
#         return super(PaginaRegistroProfesor, self).form_valid(form)

#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('usuario_profesor')
#         return super(PaginaRegistroProfesor, self).get(*args, **kwargs)
    
    

#
# class ListaPendientes(LoginRequiredMixin, ListView):
#     model = usuarios
#     context_object_name = 'usuarios'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['usuarios'] = context['usuarios'].filter(usuarios=self.request.user)
#         context['count'] = context['usuarios'].filter(completo=False).count()
#
#         valor_buscado = self.request.GET.get('area-buscar') or ''
#         if valor_buscado:
#             context['usuarios'] = context['usuarios'].filter(titulo__icontains=valor_buscado)
#             context['valor_buscado'] = valor_buscado
#         return context


class DetalleUsuarioEstudiante(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'prueba'
    template_name = 'usuario/prueba.html'
    
class DetalleUsuarioProfesor(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'prueba_profesor'
    template_name = 'usuario/prueba_profesor.html'


class CrearUsuario(LoginRequiredMixin, CreateView):
    model = usuarios
    fields = ['nombre', 'primer_apellido', 'segundo_apellido','segundo_apellido']
    success_url = reverse_lazy('usuario')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearUsuario, self).form_valid(form)


# class EditarTarea(LoginRequiredMixin, UpdateView):
#     model = Usuarios
#     fields = ['titulo', 'descripcion', 'completo']
#     success_url = reverse_lazy('tareas')
#
#
# class EliminarTarea(LoginRequiredMixin, DeleteView):
#     model = Usuarios
#     context_object_name = 'usuario'
#     success_url = reverse_lazy('tareas')


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


def password_reset_view(request):
    if request.method == 'POST':
        correo = ''
        form = PasswordResetForm(request.POST)
        cedula = '117580049'
        
        if form.is_valid():
            # cedula = request.GET.('username')
            user = User.objects.get(username=cedula)
            user_id = user.pk
            login = get_object_or_404(usuarios, id=user_id) 
            
            if login.Tipo == '1':
                profesordata = get_object_or_404(profesor, id_profesor=login.id)
                correo = profesordata.correo_profesor         
            elif login.Tipo == '2':
                estudiantedata = get_object_or_404(estudiantes, id_estudiante=login.id)
                correo = estudiantedata.correo_estudiante   
                         
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            http = 'http'
            domain = '127.0.0.1:8000'
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            reset_link = '{}://{}{}'.format(http, domain, reset_url)
            send_mail(
                'Password Reset Request',
                'Follow the link to reset your password: {}'.format(reset_link),
                settings.DEFAULT_FROM_EMAIL,
                [correo],
                fail_silently=False,
            )
        return redirect('password_reset_send')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset.html', {'form': form, 'http': 'http', 'domain': '127.0.0.1:8000'})