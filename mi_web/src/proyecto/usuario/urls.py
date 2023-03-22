from django.urls import path
from .views import  Logueo, PaginaRegistroEstudiante,PaginaRegistroProfesor,CrearUsuario,DetalleUsuario
from django.contrib.auth.views import LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.contrib.auth import views as auth_views

urlpatterns = [path('', Logueo.as_view(), name='login'),
               path('registro_estudiantes/', PaginaRegistroEstudiante.as_view(), name='registro_estudiantes'),
               path('registro_profesor/', PaginaRegistroProfesor.as_view(), name='registro_profesor'),
               path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
               path('crear-usuario/', CrearUsuario.as_view(), name='crear-usuario'),
               path('usuario/', DetalleUsuario.as_view(), name='usuario'),
               path('password-reset/', PasswordResetView.as_view(template_name='usuario/registration/password-reset.html',html_email_template_name='usuario/registration/password-reset.html'),name='password-reset'),
               path('password-reset/done/', PasswordResetDoneView.as_view(template_name='proyecto/usuario/registration/password-reset-send.html'),name='password-reset-send'),
               path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='usuario/templates/registration/password_reset_confirm.html'),name='password_reset_confirm'),
               path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='usuario/templates/registration/password_reset_complete.html'),name='password_reset_complete'),   ]

               # path('editar-tarea/<int:pk>', EditarTarea.as_view(), name='editar-tarea'),
               # path('eliminar-tarea/<int:pk>', EliminarTarea.as_view(), name='eliminar-tarea')]
