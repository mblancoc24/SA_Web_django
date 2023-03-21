from django.urls import path
from .views import  Logueo, PaginaRegistroEstudiante,PaginaRegistroProfesor,CrearUsuario,DetalleUsuario
from django.contrib.auth.views import LogoutView

urlpatterns = [path('', Logueo.as_view(), name='login'),
               path('registro_estudiantes/', PaginaRegistroEstudiante.as_view(), name='registro_estudiantes'),
               path('registro_profesor/', PaginaRegistroProfesor.as_view(), name='registro_profesor'),
               path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
               path('crear-usuario/', CrearUsuario.as_view(), name='crear-usuario'),
               path('usuario/', DetalleUsuario.as_view(), name='usuario'),]

               # path('editar-tarea/<int:pk>', EditarTarea.as_view(), name='editar-tarea'),
               # path('eliminar-tarea/<int:pk>', EliminarTarea.as_view(), name='eliminar-tarea')]
