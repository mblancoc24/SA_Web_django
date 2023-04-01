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
                    vistaPerfil,
                    cambiarcontrasena,
                    DetalleArchivoOdoo,
                    obtener_datos,
                    carrerasselect,
                    colegiosselect,
                    posgradosselect,
                    guardar_perfil,
                    enviar_archivo_a_odoo
                    )
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [path('', Logueo.as_view(), name='login'),
               path('registro_estudiantes/', PaginaRegistroEstudiante.as_view(), name='registro_estudiantes'),
               path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
               path('crear-usuario/', CrearUsuario.as_view(), name='crear-usuario'),
               path('cambiar_contrasena/', cambiarcontrasena.cambiar_contrasena, name='cambiar_contrasena'),
               
               path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
               path('password_reset/done/', MyPasswordResetDoneView.as_view(), name='password_reset_done'),

               path('usuario-estudiante/', DetalleUsuarioEstudiante.as_view(), name='usuario_estudiante'),
               path('usuario-estudiante-profesor/', DetalleUsuarioEstudianteProfesor.as_view(), name='usuario_estudiante_profesor'),
               path('usuario-profesor/', DetalleUsuarioProfesor.as_view(), name='usuario_profesor'),
               path('usuario-prospecto/', DetalleUsuarioProspecto.as_view(), name='usuario_prospecto'),
               path('obtener-datos/', obtener_datos, name='obtener_datos'),
               
               path('carrerasselect/', carrerasselect, name='carrerasselect'),
               path('colegiosselect/', colegiosselect, name='colegiosselect'),
               path('posgradosselect/', posgradosselect, name='posgradosselect'),
               
               path('perfil/', vistaPerfil.profile_view, name='perfil'),
               path('guardar-perfil/', guardar_perfil, name='guardar_perfil'),
               
               path('enviar-archivo-a-odoo/', enviar_archivo_a_odoo, name='enviar_archivo_a_odoo'),
               path('archivos-odoo/', DetalleArchivoOdoo.as_view(), name='archivos_odoo'),
               ]
