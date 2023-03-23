from django.urls import path
from .views import  Logueo, PaginaRegistroEstudiante,PaginaRegistroProfesor,CrearUsuario, DetalleUsuarioEstudiante, DetalleUsuarioProfesor, obtener_datos,password_reset_view
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [path('', Logueo.as_view(), name='login'),
               path('registro_estudiantes/', PaginaRegistroEstudiante.as_view(), name='registro_estudiantes'),
               path('registro_profesor/', PaginaRegistroProfesor.as_view(), name='registro_profesor'),
               path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
               path('crear-usuario/', CrearUsuario.as_view(), name='crear-usuario'),
               path('password_reset/', password_reset_view, name='password_reset'),
               path('password_reset_send/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_send.html'),name='password_reset_send'),
               path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html'),name='password_reset_confirm'),
               path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),   


               path('usuario-estudiante/', DetalleUsuarioEstudiante.as_view(), name='usuario_estudiante'),
               path('usuario-profesor/', DetalleUsuarioProfesor.as_view(), name='usuario_profesor'),
               path('obtener-datos/', obtener_datos, name='obtener_datos')]
