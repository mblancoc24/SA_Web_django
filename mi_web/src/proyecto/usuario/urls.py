from django.urls import path
from .payment import(
                    obtener_keyiD,
                    obtener_hash_entrada,
                    PaymentApproved,
                    )
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
                    solicitud_form,
                    user_status,
                    )
from .save_processes import(
                    payment_update_user_prospecto
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
                    enviar_archivo_posgrado,
                    enviar_archivo_cursolibre,
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
                    PaymentProspecto,
                    PaymentEstudiante,
                    HorarioPlanDeEstudioView,
                    Ubicacion,
                    Contactenos,
                    EnvioPrematricula,
                    Politicas,
                    Terminos,
                    EnvioDeConsultas,
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
               
               path('<str:type>/<int:id>/<int:status>', DetalleUsuarioProspecto.as_view(), name='usuario_prospecto'),
               path('<str:type>/<int:id>/<int:status>/perfil/', vistaPerfil.profile_view, name='perfil_prospecto'),
               
               path('obtener-datos/', obtener_datos, name='obtener_datos'),
               path('obtener-provincia/', obtener_provincia, name='obtener_provincia'),
               path('obtener-canton/', obtener_canton, name='obtener_canton'),
               path('obtener-distrito/', obtener_distrito, name='obtener_distrito'),
               path('obtener-nacionalidad/', obtener_nacionalidad, name='obtener_nacionalidad'),

               path('enviar-solicitud/', enviar_solicitud, name='enviar_solicitud'),
               
               path('<str:type>/<int:id>/<int:status>/enviar-archivo-a-odoo/', enviar_archivo_a_odoo, name='enviar_archivo_a_odoo'),
               path('<str:type>/<int:id>/<int:status>/enviar-archivo-posgrado/', enviar_archivo_posgrado, name='enviar_archivo_posgrado'),
               path('<str:type>/<int:id>/<int:status>/enviar-archivo-cursolibre/', enviar_archivo_cursolibre, name='enviar_archivo_cursolibre'),

               path('mostrar-foto/', mostrar_foto, name='mostrar_foto'),
               path('cambiar-foto/', cambiar_foto, name='cambiar_foto'),
               
               path('<str:type>/<int:id>/<int:status>/', DashboardEstudianteView.as_view(), name='estudiante'),
               path('<str:type>/<int:id>/<int:status>/perfil/', vistaPerfil.profile_view, name='perfil'),
               
               path('<str:type>/<int:id>/<int:status>/', DashboardProfesorView.as_view(), name='profesor'),
               path('<str:type>/<int:id>/<int:status>/perfil/', vistaPerfil.profile_view, name='perfil_profesor'),
               
               path('cambio-correo/', change_email, name='cambio_correo'),
               path('change-email-correct/', change_email_correct, name='change_email_correct'),
               
               path("<str:type>/<int:id>/<int:status>/revision-form/", RevisionFormView.as_view(), name="revision_form"),

               path("corregir-data/", corregirdata, name="corregir_data"),
               path("documents-status/", documents_status, name="documents_status"),
               path("user-update/", user_update, name="user_update"),
               path("solicitud-form/", solicitud_form, name="solicitud_form"),
               path("user-status/", user_status, name="user_status"),

               path("<str:type>/<int:id>/<int:status>/horario/", HorarioEstudianteView.horario_view, name='horarioEstudiante'),
               path("<str:type>/<int:id>/<int:status>/plan/", PlanDeEstudioView.as_view(), name='planEstudio'),
               path("<str:type>/<int:id>/<int:status>/plan/carrera/", DetallePlanDeEstudioView.getPlan, name='planEstudioCarrera'),
               path("<str:type>/<int:id>/<int:status>/misCursos/", MisCursos.misCursos_view, name='misCursos'),
               path("<str:type>/<int:id>/<int:status>/matricula/", MatriculaView.as_view(), name='matricula'),
               path("<str:type>/<int:id>/<int:status>/suficiencia/", SuficienciaView.as_view(), name='suficiencia'),
               
               path("descargar-archivo/<int:id>/", descargar_archivo, name="descargar_archivo"),
               path("<str:type>/<int:id>/<int:status>/estadoCuenta/", EstadoDeCuentaEstudiante.as_view(), name='estadoCuentaEstudiante'),
               path('codigoVerificacion/', codigoVerificacion, name='codigoVerificacion'),

               path("<str:type>/<int:id>/<int:status>/pagarMatricula/", PaymentProspecto.as_view(), name='payment_prospecto'),
               path("<str:type>/<int:id>/<int:status>/pagarMatricula/", PaymentEstudiante.as_view(), name='payment_estudiante'),
               path("obtener-time/", obtener_fecha_unix, name='obtener_time'),
               path("obtener-key/", obtener_keyiD, name='obtener_key'),
               path("hash-entrada/", obtener_hash_entrada, name='hash_entrada'),
               path("<str:type>/<int:id>/<int:status>/pago-realizado/", PaymentApproved.as_view(), name='pago_realizado'),

               path("estudiante/<int:id>/<int:status>/plan/cursoPlanHorario/", HorarioPlanDeEstudioView.getHorario, name='horarioCursoPlan'),
               path("<str:type>/<int:id>/<int:status>/ubicacion/", Ubicacion.ubicacion_view, name='ubicacion'),
               path("<str:type>/<int:id>/<int:status>/contactenos/", Contactenos.contactenos_view, name='contactenos'),
               path("<str:type>/<int:id>/<int:status>/plan/envioPrematricula/", EnvioPrematricula.envioPrematricula, name='envioPrematricula'),

               path("<str:type>/<int:id>/pago-finalizado/", payment_update_user_prospecto, name='pago_finalizado'),
               
               path("<str:type>/<int:id>/<int:status>/politicas/", Politicas.politicas_view, name='politicas'),
               path("<str:type>/<int:id>/<int:status>/terminos/", Terminos.terminos_view, name='terminos'),
               path("<str:type>/<int:id>/<int:status>/envioConsulta/", EnvioDeConsultas.envioDeConsultas, name='envioConsulta'),
               ]