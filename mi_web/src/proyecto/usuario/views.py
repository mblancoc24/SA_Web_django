from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .formulario_estudiante import FormularioEstudiantes
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import usuarios


class Logueo(LoginView):
    template_name = 'usuario/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('usuario')


class PaginaRegistroEstudiante(FormView):
    template_name = 'usuario/registro_estudiantes.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        username_estudiantes = form.cleaned_data['username']
        password_estudiantes = form.cleaned_data['password2']
        nombre_estudiante = self.request.POST.get('nombre')
        primerapellido = self.request.POST.get('primerapellido')
        segundoapellido = self.request.POST.get('segundoapellido')
        fecha = self.request.POST.get('fechanacimiento')
        telefono = self.request.POST.get('telefono')
        correo = self.request.POST.get('correo')
        
        datos_estudiante = [username_estudiantes,password_estudiantes,nombre_estudiante,
                            primerapellido,segundoapellido,fecha,telefono,correo]
        
        Usuarios = form.save() # type: ignore
        
        form = FormularioEstudiantes(self.request.POST)
        form.save() # type: ignore
            
        if Usuarios is not None:
            login(self.request, Usuarios)
        return super(PaginaRegistroEstudiante, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('usuario')
        return super(PaginaRegistroEstudiante, self).get(*args, **kwargs)

class PaginaRegistroProfesor(FormView):
    template_name = 'usuario/registro_profesor.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('usuario')

    def form_valid(self, form):
        Usuarios = form.save() # type: ignore
        if Usuarios is not None:
            login(self.request, Usuarios)
        return super(PaginaRegistroProfesor, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('usuario')
        return super(PaginaRegistroProfesor, self).get(*args, **kwargs)
    
    

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


class DetalleUsuario(LoginRequiredMixin, ListView):
    model = usuarios
    context_object_name = 'prueba'
    template_name = 'usuario/prueba.html'


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
