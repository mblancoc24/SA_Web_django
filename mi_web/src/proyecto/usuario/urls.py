from django.urls import path
from .api_queries import(
                    obtener_datos,
                    obtener_provincia,
                    obtener_canton,
                    obtener_distrito,
                    obtener_nacionalidad,
                    obtener_fecha_unix,
                    )
from .api_processes import (
                    documents_status,
                    user_update,
                    )
from .views import (
                    Logueo, 
                    PaginaRegistroEstudiante,
                    DetalleUsuarioEstudianteProfesor, 
                    DetalleUsuarioEstudiante, 
                    DetalleUsuarioProfesor, 
                    DetalleUsuarioProspecto,
                    vistaPerfil,
                    carrerasselect,
                    colegiosselect,
                    posgradosselect,
                    guardar_perfil,
                    enviar_archivo_a_odoo,
                    enviar_solicitud,
                    mostrar_foto,
                    cambiar_foto,
                    change_email,
                    change_email_correct,
                    corregirdata,
                    microsoft_auth, 
                    microsoft_callback,
                    descargar_archivo,
                    DashboardEstudianteView,
                    DashboardProfesorView,
                    MicrosoftLogoutView,
                    HorarioEstudianteView,
                    PlanDeEstudioView,
                    DetallePlanDeEstudioView,
                    MatriculaView,
                    MisCursos,
                    EstadoDeCuentaEstudiante,
                    codigoVerificacion,
                    SuficienciaView,
                    RevisionFormView,
                    Payment,
                    )
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [path('', Logueo.as_view(), name='login'),
               path('registro_estudiantes/', PaginaRegistroEstudiante.as_view(), name='registro_estudiantes'),
               path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
               
               path('microsoft-auth/', microsoft_auth, name='microsoft_auth'),
               path('microsoft-callback/', microsoft_callback, name='microsoft_callback'),
               
               path('logout/', MicrosoftLogoutView.as_view(), name='logout'),
             
               path(
                'change-password/',
                auth_views.PasswordChangeView.as_view(
                    template_name='Contrasenas/Correo/change-password.html',
                    success_url = '/logout/'
                ),
                name='change_password'
                ),
               
               path('password-reset/',
                auth_views.PasswordResetView.as_view(
                template_name='Contrasenas/Correo/password_reset.html',
                subject_template_name='Contrasenas/Correo/password_reset_subject.txt',
                email_template_name='Contrasenas/Correo/password_reset_email.html'),
                name='password_reset'),
               
                path('password-reset/done/',
                    auth_views.PasswordResetDoneView.as_view(
                        template_name='Contrasenas/Correo/password_reset_done.html'
                    ),
                    name='password_reset_done'),
                
                path('password-reset-confirm/<uidb64>/<token>/',
                    auth_views.PasswordResetConfirmView.as_view(
                        template_name='Contrasenas/Correo/password_reset_confirm.html'
                    ),
                    name='password_reset_confirm'),
                
                path('password-reset-complete/',
                    auth_views.PasswordResetCompleteView.as_view(
                        template_name='Contrasenas/Correo/password_reset_complete.html'
                    ),
                    name='password_reset_complete'),
                
                path('carrerasselect/', carrerasselect, name='carrerasselect'),
                path('colegiosselect/', colegiosselect, name='colegiosselect'),
                path('posgradosselect/', posgradosselect, name='posgradosselect'),
               
               path('usuario-estudiante/', DetalleUsuarioEstudiante.as_view(), name='usuario_estudiante'),
               path('usuario-estudiante-profesor/', DetalleUsuarioEstudianteProfesor.as_view(), name='usuario_estudiante_profesor'),
               path('usuario-profesor/', DetalleUsuarioProfesor.as_view(), name='usuario_profesor'),
               
               path('prospecto/<int:id>/<int:status>', DetalleUsuarioProspecto.as_view(), name='usuario_prospecto'),
               path('prospecto/<int:id>/<int:status>/perfil/', vistaPerfil.profile_view, name='perfil_prospecto'),
               
               path('obtener-datos/', obtener_datos, name='obtener_datos'),
               path('obtener-provincia/', obtener_provincia, name='obtener_provincia'),
               path('obtener-canton/', obtener_canton, name='obtener_canton'),
               path('obtener-distrito/', obtener_distrito, name='obtener_distrito'),
               path('obtener-nacionalidad/', obtener_nacionalidad, name='obtener_nacionalidad'),

               path('enviar-solicitud/', enviar_solicitud, name='enviar_solicitud'),
               
               path('prospecto/<int:id>/<int:status>/enviar-archivo-a-odoo/', enviar_archivo_a_odoo, name='enviar_archivo_a_odoo'),
               
               path('mostrar-foto/', mostrar_foto, name='mostrar_foto'),
               path('cambiar-foto/', cambiar_foto, name='cambiar_foto'),
               
               path('estudiante/<int:id>/<int:status>/', DashboardEstudianteView.as_view(), name='estudiante'),
               path('estudiante/<int:id>/<int:status>/perfil/', vistaPerfil.profile_view, name='perfil'),
               
               path('profesor/<int:id>/<int:status>/', DashboardProfesorView.as_view(), name='profesor'),
               path('profesor/<int:id>/<int:status>/perfil/', vistaPerfil.profile_view, name='perfil_profesor'),
               
               path('cambio-correo/', change_email, name='cambio_correo'),
               path('change-email-correct/', change_email_correct, name='change_email_correct'),
               
               path("prospecto/<int:id>/<int:status>/revision-form/", RevisionFormView.as_view(), name="revision_form"),
               path("corregir-data/", corregirdata, name="corregir_data"),
               path("documents-status/", documents_status, name="documents_status"),
               path("user-update/", user_update, name="user_update"),
               path("prospecto/<int:id>/<int:status>/horario/", HorarioEstudianteView.horario_view, name='horarioEstudiante'),
               path("prospecto/<int:id>/<int:status>/plan/", PlanDeEstudioView.as_view(), name='planEstudio'),
               path("prospecto/<int:id>/<int:status>/plan/carrera/", DetallePlanDeEstudioView.getPlan, name='planEstudioCarrera'),
               path("prospecto/<int:id>/<int:status>/misCursos/", MisCursos.misCursos_view, name='misCursos'),
               path("prospecto/<int:id>/<int:status>/matricula/", MatriculaView.as_view(), name='matricula'),
               path("prospecto/<int:id>/<int:status>/suficiencia/", SuficienciaView.as_view(), name='suficiencia'),
               
               path("descargar-archivo/<int:id>/", descargar_archivo, name="descargar_archivo"),
               path("prospecto/<int:id>/<int:status>/estadoCuenta/", EstadoDeCuentaEstudiante.as_view(), name='estadoCuentaEstudiante'),
               path('codigoVerificacion/', codigoVerificacion, name='codigoVerificacion'),
               path("prospecto/<int:id>/<int:status>/pagarMatricula/", Payment.as_view(), name='payment'),
               path("obtener-time/", obtener_fecha_unix, name='obtener_time'),
               ]


