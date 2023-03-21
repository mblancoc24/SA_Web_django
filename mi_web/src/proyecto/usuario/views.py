from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
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
    success_url = reverse_lazy('usuario')

    def form_valid(self, form):
        Usuarios = form.save()
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
        Usuarios = form.save()
        if Usuarios is not None:
            login(self.request, Usuarios)
        return super(PaginaRegistro, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('Usuario')
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


# class DetalleTarea(LoginRequiredMixin, DetailView):
#     model = Usuarios
#     context_object_name = 'usuario'
#     template_name = 'usuario/usuario.html'
#
#
# class CrearTarea(LoginRequiredMixin, CreateView):
#     model = Usuarios
#     fields = ['titulo', 'descripcion', 'completo']
#     success_url = reverse_lazy('tareas')
#
#     def form_valid(self, form):
#         form.instance.usuario = self.request.user
#         return super(CrearTarea, self).form_valid(form)
#
#
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
