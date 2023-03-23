from django.urls import path
from .views import  Logueo, PaginaRegistroEstudiante,PaginaRegistroProfesor,CrearUsuario, DetalleUsuarioEstudiante, DetalleUsuarioProfesor, obtener_datos
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [path('', Logueo.as_view(), name='login'),
               path('registro_estudiantes/', PaginaRegistroEstudiante.as_view(), name='registro_estudiantes'),
               path('registro_profesor/', PaginaRegistroProfesor.as_view(), name='registro_profesor'),
               path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
               path('crear-usuario/', CrearUsuario.as_view(), name='crear-usuario'),
               path('password-reset/',auth_views.PasswordResetView.as_view(template_name='registration/password-reset.html',html_email_template_name='registration/password-reset-email.html'),name='password-reset'),
               path('password-reset-send/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset-send.html'),name='password-reset-send'),
               path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html'),name='password-reset-confirm'),
               path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset-complete.html'),name='password-reset-complete'),   


               path('usuario-estudiante/', DetalleUsuarioEstudiante.as_view(), name='usuario_estudiante'),
               path('usuario-profesor/', DetalleUsuarioProfesor.as_view(), name='usuario_profesor'),
               path('obtener-datos/', obtener_datos, name='obtener_datos')]
