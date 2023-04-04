from django.urls import path
from .views import (MyPasswordResetView, 
                    MyPasswordResetDoneView,
                    MyPasswordResetView, 
                    MyPasswordResetConfirmView,
                    PasswordResetCompleteView,
                    Logueo, 
                    PaginaRegistroEstudiante,
                    CrearUsuario, 
                    DetalleUsuarioEstudianteProfesor, 
                    DetalleUsuarioEstudiante, 
                    DetalleUsuarioProfesor, 
                    DetalleUsuarioProspecto,
                    vistaPerfil,
                    cambiarcontrasena,
                    SessionTimeoutView,
                    obtener_datos,
                    obtener_provincia,
                    obtener_canton,
                    obtener_distrito,
                    obtener_nacionalidad,
                    carrerasselect,
                    colegiosselect,
                    posgradosselect,
                    guardar_perfil,
                    enviar_archivo_a_odoo,
                    mostrar_foto,
                    )
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [path('', Logueo.as_view(), name='login'),
               path('registro_estudiantes/', PaginaRegistroEstudiante.as_view(), name='registro_estudiantes'),
               path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
               path('crear-usuario/', CrearUsuario.as_view(), name='crear-usuario'),
               path('cambiar_contrasena/', cambiarcontrasena.cambiar_contrasena, name='cambiar_contrasena'),
               
               path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
               path('password_reset_done/', MyPasswordResetDoneView.as_view(), name='password_reset_done'),
               path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
               path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
               path('usuario-estudiante/', DetalleUsuarioEstudiante.as_view(), name='usuario_estudiante'),
               path('usuario-estudiante-profesor/', DetalleUsuarioEstudianteProfesor.as_view(), name='usuario_estudiante_profesor'),
               path('usuario-profesor/', DetalleUsuarioProfesor.as_view(), name='usuario_profesor'),
               path('usuario-prospecto/', DetalleUsuarioProspecto.as_view(), name='usuario_prospecto'),
               
               path('obtener-datos/', obtener_datos, name='obtener_datos'),
               path('obtener-provincia/', obtener_provincia, name='obtener_provincia'),
               path('obtener-canton/', obtener_canton, name='obtener_canton'),
               path('obtener-distrito/', obtener_distrito, name='obtener_distrito'),
               path('obtener-nacionalidad/', obtener_nacionalidad, name='obtener_nacionalidad'),
               
               path('carrerasselect/', carrerasselect, name='carrerasselect'),
               path('colegiosselect/', colegiosselect, name='colegiosselect'),
               path('posgradosselect/', posgradosselect, name='posgradosselect'),
               
               path('perfil/', vistaPerfil.profile_view, name='perfil'),
               path('guardar-perfil/', guardar_perfil, name='guardar_perfil'),
               
               path('enviar-archivo-a-odoo/', enviar_archivo_a_odoo, name='enviar_archivo_a_odoo'),
               path('mostrar-foto/', mostrar_foto, name='mostrar_foto'),
               ]
