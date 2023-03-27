from django.urls import path
from .views import (MyPasswordResetView, 
                    MyPasswordResetDoneView, 
                    Logueo, 
                    PaginaRegistroEstudiante,
                    CrearUsuario, 
                    DetalleUsuarioEstudianteProfesor, 
                    DetalleUsuarioEstudiante, 
                    DetalleUsuarioProfesor, 
                    DetalleUsuarioProspecto,
                    obtener_datos,
                    cambiar_contrasena)
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [path('', Logueo.as_view(), name='login'),
               path('registro_estudiantes/', PaginaRegistroEstudiante.as_view(), name='registro_estudiantes'),
               path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
               path('crear-usuario/', CrearUsuario.as_view(), name='crear-usuario'),
               path('cambiar_contrasena/', cambiar_contrasena, name='cambiar_contrasena'),
               
               path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
               path('password_reset/done/', MyPasswordResetDoneView.as_view(), name='password_reset_done'),

               path('usuario-estudiante/', DetalleUsuarioEstudiante.as_view(), name='usuario_estudiante'),
               path('usuario-estudiante-profesor/', DetalleUsuarioEstudianteProfesor.as_view(), name='usuario_estudiante_profesor'),
               path('usuario-profesor/', DetalleUsuarioProfesor.as_view(), name='usuario_profesor'),
               path('usuario-prospecto/', DetalleUsuarioProspecto.as_view(), name='usuario_prospecto'),
               path('obtener-datos/', obtener_datos, name='obtener_datos'),
               ]
