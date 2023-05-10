from django.shortcuts import render, redirect, get_object_or_404
from .models import profesor, estudiantes, RegistroLogsUser, documentos, carreras, colegios, posgrados, fotoperfil, estados, primerIngreso, prospecto
from .forms import FormularioEstudiantes, FormularioDocumentos, FormularioPrimerIngreso, FormularioProfesor, FormularioProspecto, FormularioInfoEstudiante, CustomUserCreationForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image
import requests
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
import random
from django.urls import reverse
from .backends import MicrosoftGraphBackend
from .dspace_processes import dspace_processes
from .save_processes import save_profile_processes
from .api_queries import enviar_data_odoo, insert_urls, get_urls
from django.core.cache import cache
import json
from datetime import datetime
import base64

class Logueo(LoginView):
    template_name = 'usuario/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cuenta'] = self.request.GET.get('cuenta')
        return context

    def form_valid(self, form):
        logout(self.request)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user = authenticate(self.request, username=username, password=password)
        
        prospecto_user = get_object_or_404(prospecto, identificacion=user.username)
        prospecto_dict = {}
        for field in prospecto._meta.get_fields():
            field_name = field.name
            if field_name != 'info_estudiantes' and field_name != 'fecha_nacimiento':
                field_value = getattr(prospecto_user, field_name)
                prospecto_dict[field_name] = field_value
            elif field_name == 'fecha_nacimiento':
                field_value = getattr(prospecto_user, field_name)
                fecha_str = field_value.strftime('%Y-%m-%d')
                prospecto_dict[field_name] = fecha_str
        
        prospecto_dict['tipo'] = 'prospecto'
            
        self.request.session['user_info'] = prospecto_dict
        
        if user is None:
            form.add_error('username', 'El usuario no existe en el sistema')
            logout(self.request)
            return super().form_invalid(form)
        else:
            login(self.request, user)
            registrar_accion(user, 'El usuario {0} ha ingresado como prospecto.'.format(user.username))
            context = {'id': username, 'status': 4}
            return redirect(reverse('usuario_prospecto', kwargs=context))

def microsoft_auth(request):
    # Comprobar si ya existe una sesión de usuario
    if 'access_token' in request.session:
        url = "https://graph.microsoft.com/v1.0/me"
        bearer = 'Bearer ' + request.session['access_token']
        headers = {
            'Authorization': bearer
        }
        access_token = request.session['access_token']
        requests_response = requests.get(url, headers=headers)
        
        if requests_response.status_code == 200:
            user = MicrosoftGraphBackend.authenticate(request=request, access_token=access_token)
            tipo_user = request.session.get('user_info')
            
            if user is not None and tipo_user is not None:
                if user.is_active:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    if tipo_user['tipo'] == 'estudiante':
                        registrar_accion(user, 'El usuario {0} ha ingresado como estudiante.'.format(user.username))
                        context = {'id': user.username, 'status': 1}
                        return redirect(reverse('estudiante', kwargs=context))
                    
                    elif tipo_user['tipo'] == 'profesor' or tipo_user['tipo'] == 'prospecto/profesor':
                        registrar_accion(user, 'El usuario {0} ha ingresado como profesor.'.format(user.username))
                        context = {'id': user.username, 'status': 2}
                        return redirect(reverse('profesor', kwargs=context))
                    
                    elif tipo_user['tipo'] == 'estudiante/profesor':
                        registrar_accion(user, 'El usuario {0} ha ingresado como estudiante/profesor.'.format(user.username))
                        context = {'id': user.username, 'status': 3}
                        return redirect(reverse('profesor', kwargs=context))
        else:
            del request.session['access_token']
            return redirect('login')
    else:
        redirect_uri = request.build_absolute_uri(settings.MICROSOFT_AUTH_REDIRECT_URI)
        params = {
            'client_id': settings.MICROSOFT_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'response_mode': 'query'
        }
        url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
        return redirect(f"{url}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&response_type={params['response_type']}&scope={params['scope']}&response_mode={params['response_mode']}")

def microsoft_callback(request):
    auth_code = request.GET.get('code')
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    redirect_uri = request.build_absolute_uri(settings.MICROSOFT_AUTH_REDIRECT_URI)
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': settings.MICROSOFT_CLIENT_ID,
        'client_secret': settings.MICROSOFT_CLIENT_SECRET,
        'scope': 'openid email profile'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    requests_response = requests.post(url, data=data, headers=headers)
    if requests_response.status_code == 200:
        
        response_json = requests_response.json()
        request.session['access_token'] = response_json['access_token']
        access_token = response_json['access_token']
        token_type = requests_response.json().get('token_type')
        
        user = MicrosoftGraphBackend.authenticate(request=request, access_token=access_token)
        tipo_user = request.session.get('user_info')
        
        if user is not None and tipo_user is not None:
            if user.is_active:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if tipo_user['tipo'] == 'estudiante':
                    registrar_accion(user, 'El usuario {0} ha ingresado como estudiante.'.format(user.username))
                    context = {'id': user.username, 'status': 1}
                    return redirect(reverse('estudiante', kwargs=context))
                
                elif tipo_user['tipo'] == 'profesor' or tipo_user['tipo'] == 'prospecto/profesor':
                    registrar_accion(user, 'El usuario {0} ha ingresado como profesor.'.format(user.username))
                    context = {'id': user.username, 'status': 2}
                    return redirect(reverse('profesor', kwargs=context))
                
                elif tipo_user['tipo'] == 'estudiante/profesor':
                    registrar_accion(user, 'El usuario {0} ha ingresado como estudiante/profesor.'.format(user.username))
                    context = {'id': user.username, 'status': 3}
                    return redirect(reverse('profesor', kwargs=context))
    else:
        return redirect('login')
    
class MicrosoftLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logged_out.html'
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'access_token' in request.session:
                # Hacer una solicitud de cierre de sesión a través de la API de Microsoft Graph
                    
                headers = {
                    "Authorization": "Bearer " + request.session['access_token'],
                    "Content-Type": "application/json"
                }
                
                client_id = settings.MICROSOFT_CLIENT_ID
                redirect_uri = 'http://localhost:8000/microsoft-callback/'
                
                revoke_url = f'https://login.live.com/oauth20_logout.srf?client_id='+client_id+'&redirect_uri='+redirect_uri
                response = requests.post(revoke_url, headers=headers)
                
                if response.status_code == 200:
                    request.session.flush()
                    cache.clear()
                    print("Se ha cerrado sesión correctamente.")
                else:
                    print("Error al cerrar sesión.")

        return super().dispatch(request, *args, **kwargs)

    def get_next_page(self):
        next_page = super().get_next_page()
        if next_page == self.request.path:
            return self.next_page
        else:
            return next_page

class PaginaRegistroEstudiante(FormView):
    template_name = 'usuario/registro_estudiantes.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        username = form.cleaned_data['username']
        nombre_estudiante = self.request.POST.get('first_name')
        primerapellido = self.request.POST.get('last_name')
        segundoapellido = self.request.POST.get('segundoapellido')
        fecha = self.request.POST.get('fechanacimiento')
        telefono = self.request.POST.get('telefono')
        telefono2 = self.request.POST.get('telefono2')
        correo_personal = self.request.POST.get('email')
        nacionalidad = self.request.POST.get('pais')
        provincia = self.request.POST.get('provincia')
        canton = self.request.POST.get('canton')
        distrito = self.request.POST.get('distrito')
        direccion_exacta = self.request.POST.get('direccion_exacta')
        sexo = self.request.POST.get('Genero_select')
        
        Usuarios = form.save()

        datos_estudiante = [username, nombre_estudiante, primerapellido,
            segundoapellido, fecha, telefono, telefono2, 'No Asignado', correo_personal, 
            nacionalidad, provincia, canton, distrito, direccion_exacta, sexo]

        save = save_profile_processes.save_prospecto(self.request, datos_estudiante)
        
        if save:
            user = User.objects.get(username=username)
            
            if user is not None:
                
                subject = 'Se ha creado su cuenta satisfactoriamente'
                message = f'Bienvenido al portal academico UIA, su cuenta se ha creado satisfactoriamente con el usuario {user.username}, Saludos cordiales.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail(subject, message, email_from, recipient_list)
                
                login(self.request, user)
                
                registrar_accion(user, 'El usuario '+ username +' se ha creado una cuenta como prospecto.')
                
                logout(self.request)
                
                # Agrega el contexto con el valor 'cuenta' para enviarlo junto con la redirección.
                url = reverse('login') + '?cuenta=True'
                return redirect(url)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
            return redirect('registro_estudiantes')
        return super(PaginaRegistroEstudiante, self).get(*args, **kwargs)

class DetalleUsuarioEstudiante(LoginRequiredMixin, ListView):
    context_object_name = 'prueba_estudiante'
    template_name = 'Dashboard/Estudiante/prueba_estudiante.html'

class DetalleUsuarioProfesor(LoginRequiredMixin, ListView):
    context_object_name = 'prueba_profesor'
    template_name = 'Dashboard/Profesor/prueba_profesor.html'

class DetalleUsuarioProspecto(LoginRequiredMixin, ListView):
    context_object_name = 'prueba_prospecto'
    template_name = 'Dashboard/Prospecto/prospecto.html'

    def get(self, request, id, status):
        user = request.user
        try:
            fotoperfil_obj = fotoperfil.objects.get(user=user.pk)
            imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))
            context = {
                'id': id,
                'status': status,
                'user': user,
                'fotoperfil': imagen_url,
            }
        except fotoperfil.DoesNotExist:

            context = {
                'id': id,
                'status': status,
                'user': user,
            }
        return render(request, 'Dashboard/Prospecto/prospecto.html', context)

class DetalleUsuarioEstudianteProfesor(LoginRequiredMixin, ListView):
    context_object_name = 'opciones_estudiante_profesor'
    template_name = 'usuario/opciones_login.html'

class DetalleArchivoOdoo(LoginRequiredMixin, ListView):
    context_object_name = 'envio_archivos_odoo'
    template_name = 'usuario/mmgv.html'

def registrar_accion(usuario, accion):
    registro = RegistroLogsUser(usuario=usuario, accion=accion)
    registro.save()

def carrerasselect(request):
    valores = carreras.objects.values_list('nombre_carrera', flat=True)
    return JsonResponse(list(valores), safe=False)

def colegiosselect(request):
    valores = colegios.objects.values_list('nombre_colegio', flat=True)
    return JsonResponse(list(valores), safe=False)

def posgradosselect(request):
    valores = posgrados.objects.values_list('nombre_carrera', flat=True)
    return JsonResponse(list(valores), safe=False)

class vistaPerfil (LoginRequiredMixin):
    context_object_name = 'perfil_estudiante'
    template_name = 'Dashboard/Componentes/perfil.html'

    def profile_view(request, id, status):
        user = request.user
        
        login = request.session.get('user_info')
        
        if login['tipo'] == 'prospecto':
            login = get_object_or_404(prospecto, identificacion=user.username)
        
        try:
            fotoperfil_obj = fotoperfil.objects.get(user=user.pk)
            imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))
            context = {
                'user': user,
                'estudiante': login,
                'fotoperfil': imagen_url,
                'status': status,
                'id': id,
            }
        except fotoperfil.DoesNotExist:

            context = {
                'user': user,
                'estudiante': login,
                'status': status,
                'id': id,
            }
        return render(request, 'Dashboard/Componentes/perfil.html', context)

#Verificar
def guardar_perfil(request):
    if request.method == 'POST':
        user = request.user
        numero_telefonico = request.POST.get('numero_telefonico')
        numero_telefonico2 = request.POST.get('numero_telefonico2')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        distrito = request.POST.get('distrito')

        user = User.objects.get(username=user.username)
        
        user_type = MicrosoftGraphBackend.user_type(request)
    
        if user_type == 'estudiante/profesor':
            estudiante = get_object_or_404(estudiantes, identificacion=user.username)
            
            if estudiante is not None:
                datos_estudiante = [estudiante.identificacion, estudiante.nombre, estudiante.primer_apellido,
                                estudiante.segundo_apellido, estudiante.fecha_nacimiento, numero_telefonico, numero_telefonico2, estudiante.correo_institucional, estudiante.correo_personal, estudiante.nacionalidad, provincia, canton, distrito, estudiante.sexo]

                save = save_profile_processes.update_student(request, datos_estudiante)
                
                if save:
                    pass
                else:
                    print('Error en el guardado')
                    
            profesores = get_object_or_404(profesor, identificacion=user.username)
            
            if profesores is not None:
                datos_profesor = [profesores.identificacion, profesores.nombre, profesores.primer_apellido,
                              profesores.segundo_apellido, profesores.fecha_nacimiento, numero_telefonico, numero_telefonico2, profesores.correo_institucional, profesores.correo_personal, profesores.nacionalidad, provincia, canton, distrito, profesores.sexo, profesores.puesto_educativo]

                save = save_profile_processes.update_professor(request, datos_profesor)
                
                if save:
                    pass
                else:
                    print('Error en el guardado')

            return redirect(request.META.get('HTTP_REFERER'))

        elif user_type == 'prospecto/profesor':
            prospecto_user = get_object_or_404(prospecto, identificacion=user.username)
            
            if prospecto_user is not None:
                datos_prospecto = [prospecto_user.user, prospecto_user.identificacion, prospecto_user.nombre, prospecto_user.primer_apellido,
                                    prospecto_user.segundo_apellido, prospecto_user.fecha_nacimiento, numero_telefonico, numero_telefonico2, prospecto_user.correo_institucional,
                                    prospecto_user.correo_personal, prospecto_user.nacionalidad, provincia, canton, distrito, prospecto_user.sexo]

                save = save_profile_processes.update_prospecto(request, datos_prospecto)
                
                if save:
                    pass
                else:
                    print('Error en el guardado')
                
                
            profesores = get_object_or_404(profesor, identificacion=user.username)

            if profesores is not None:
                datos_profesor = [profesores.identificacion, profesores.nombre, profesores.primer_apellido,
                                profesores.segundo_apellido, profesores.fecha_nacimiento, numero_telefonico, numero_telefonico2, profesores.correo_institucional, profesores.correo_personal, profesores.nacionalidad, provincia, canton, distrito, profesores.sexo, profesores.puesto_educativo]

                save = save_profile_processes.update_professor(request, datos_profesor)
                
                if save:
                    pass
                else:
                    print('Error en el guardado')
                    
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)

def mostrar_foto(request):
    user = request.user
    foto_perfil = get_object_or_404(fotoperfil, user=user.pk)
    foto_bytes = bytes(foto_perfil.archivo)
    return HttpResponse(foto_bytes, content_type='image/png')

def cambiar_foto(request):
    user = request.user
    foto = request.FILES.get('fotocambio')
        
    img_data = foto.read()
        
    # Convertir la imagen a bytes
    img_bytes = bytearray(img_data)

    # Crear el objeto UserFile y guardarlo en la base de datos
    user_file = fotoperfil(user=user, archivo=img_bytes)
    
    try:
        img_validation = get_object_or_404(fotoperfil, user=user.pk)
        if img_validation is not None:
            img_validation.delete()
            user_file.save()
    except:
        user_file.save()
    return redirect(request.META.get('HTTP_REFERER'))

class DashboardEstudianteView(LoginRequiredMixin, View):
    login_url = ''  # Ruta de inicio de sesión
    redirect_field_name = 'login'  # Nombre del campo de redirección

    def get(self, request, id, status):
        return render(request, 'Dashboard/dashboard.html', {'id': id, 'status': status})

class DashboardProfesorView(LoginRequiredMixin, View):
    login_url = ''  # Ruta de inicio de sesión
    redirect_field_name = 'login'  # Nombre del campo de redirección

    def get(self, request, id, status):
        return render(request, 'Dashboard/dashboard.html', {'id': id, 'status': status})

def change_email(request):
    codigo = random.randint(100000, 999999)

    user = request.user
    user_email = request.session.get('user_info')
    subject = 'Cambio de Correo Electronico'
    message = f'Hola, {user.username}, se ha solicitado modificar el correo electronico personal.\n\nEl código es: {codigo}\n\nEL CODIGO SOLO ES VALIDO PARA EL DIA DE HOY.\n\nUn cordial saludo.\nUIA.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email['correo_personal'],]

    send_mail(subject, message, email_from, recipient_list)

    return render(request, 'usuario/cambio_correo_codigo.html', {'codigo': codigo})

def change_email_correct(request):
    if request.method == 'POST':
        user = request.user

        nuevo_correo = request.POST.get('nuevo_correo2')
        
        user_type = request.session.get('user_info')
        
        if user_type['tipo'] == "prospecto" or user_type['tipo'] == "prospecto/profesor":
            prospecto_user = get_object_or_404(prospecto, identificacion=user.username)
            datos_prospecto = [prospecto_user.identificacion, prospecto_user.nombre, prospecto_user.primer_apellido,
                            prospecto_user.segundo_apellido, prospecto_user.fecha_nacimiento, prospecto_user.numero_telefonico, prospecto_user.numero_telefonico2, prospecto_user.correo_institucional,
                            nuevo_correo, prospecto_user.nacionalidad, prospecto_user.provincia, prospecto_user.canton, prospecto_user.distrito, prospecto_user.sexo]

            save = save_profile_processes.update_prospecto(request, datos_prospecto)
                    
            if save:
                #ENVIAR A API ACTUALIZACION
                return redirect('perfil_prospecto')
            else:
                print('Error en el guardado')
        elif user_type['tipo'] == "estudiante":
            #ENVIAR A API ACTUALIZACION
            return redirect('perfil_prospecto')
        elif user_type['tipo'] == "profesor":
            #ENVIAR A API ACTUALIZACION
            return redirect('perfil_prospecto')
        
        prospecto_user = get_object_or_404(prospecto, identificacion=user.username)
 
def revision_formulario(request, id, status):
    user = request.user

    # Obtener el objeto de la base de datos según su ID
    statusgeneral = get_object_or_404(primerIngreso, usuario=user.pk)

    estado = get_object_or_404(estados, id_estado=statusgeneral.estado_id)

    docs = get_object_or_404(documentos, usuario=user.pk)
    
    if 'urls' in request.session:
        data_urls = request.session.get('urls')
    else:
        data_urls = get_urls(request)
        request.session['urls'] = data_urls
    
    data_content = []
    data_content_type = []
    
    if 'urlsContent' in request.session: 
        data_content = request.session.get('urlsContent')
        data_content_type = request.session.get('urlsContentType')
    else:
        responses = dspace_processes.dspace_docs_visualization(data_urls)
        
        for response in responses:
            data_content.append(base64.b64encode(response.content).decode('utf-8'))
            if 'pdf' in response.headers['Content-Type']:
                data_content_type.append('pdf')
            elif 'jpeg' in response.headers['Content-Type']:
                data_content_type.append('jpeg')
            elif 'png' in response.headers['Content-Type']:
                data_content_type.append('png')
                
        if len(data_content) == 3:
            data_content_type.append('N/A')
            data_content_type.append('N/A')
    
        request.session['urlsContent'] = data_content
        request.session['urlsContentType'] = data_content_type
        
    try:
        fotoperfil_obj = fotoperfil.objects.get(user=user.pk)
        imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))

        # Enviar el objeto y otros datos necesarios a la plantilla HTML
        contexto = {
            "fotoperfil": imagen_url,
            "comentario": statusgeneral.comentario,
            "estado": estado.estado_nombre,
            "convalidacion": statusgeneral.convalidacion,
            "documentos": docs,
            "data_content": data_content,
            "data_type":data_content_type,
            "id": id,
            "status": status,
        }
    except fotoperfil.DoesNotExist:
        contexto = {
            "comentario": statusgeneral.comentario,
            "estado": estado.estado_nombre,
            "convalidacion": statusgeneral.convalidacion,
            "documentos": docs,
            "data_content": data_content,
            "data_type":data_content_type,
            "id": id,
            "status": status,
        }
    return render(request, "Dashboard/Prospecto/revision_form.html", contexto)

def descargar_archivo(request, id):
    # Obtiene el contenido del bitstream de la API de DSpace
    responses = cache.get('urls_links')
    response = responses[id]
    # Establece el tipo de contenido según la extensión del archivo
    if 'pdf' in response.headers['Content-Type']:
        content_type = 'application/pdf'
        extension = 'pdf'
    elif 'jpeg' in response.headers['Content-Type']:
        content_type = 'image/jpeg'
        extension = 'jpg'
    elif 'png' in response.headers['Content-Type']:
        content_type = 'image/png'
        extension = 'png'
    else:
        return HttpResponse('Tipo de archivo no soportado')

    # Devuelve la respuesta como archivo descargable
    response = HttpResponse(response.content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="archivo.{extension}"'
    return response

def corregirdata(request):
    user = request.user

    datocargado = request.POST.get('documentocargado')
    
    if datocargado == 'tituloeducacion':
        file_content = request.FILES.get('titulo')
    elif datocargado == 'identificacion':
        file_content = request.FILES.get('identificacion')
    elif datocargado == 'fotoperfil':
        file_content = request.FILES.get('pasaporte')
    elif datocargado == 'record_academico':
        file_content = request.FILES.get('notas')
    elif datocargado == 'plan_estudio':
        file_content = request.FILES.get('planestudio')
        
    
    file_standardization = dspace_processes.name_file_correction_standardization(request, file_content, datocargado)
        
    save_file = dspace_processes.dspace_file_correction(request, file_standardization, datocargado)

    statusgeneral = get_object_or_404(primerIngreso, usuario=user.pk)
    docs = get_object_or_404(documentos, usuario=user.pk)

    i = 1
    doc_no_corr = 0
    while i <= 6:
        if not docs.tituloeducacion and i == 1:
            doc_no_corr += 1

        if not docs.titulouniversitario and i == 2:
            doc_no_corr += 1

        if not docs.identificacion and i == 3:
            doc_no_corr += 1

        if not docs.foto and i == 4:
            doc_no_corr += 1

        if not docs.notas and i == 5:
            doc_no_corr += 1

        if not docs.plan and i == 6:
            doc_no_corr += 1

        i += 1

    if doc_no_corr == 1:
        formulariodata = [2, 3, statusgeneral.convalidacion,
                          user.pk, statusgeneral.comentario]
    else:
        formulariodata = [2, 5, statusgeneral.convalidacion,
                          user.pk, statusgeneral.comentario]

    if datocargado == "tituloeducacion":
        formulariodocs = [user.pk, True, docs.titulouniversitario,
                          docs.identificacion, docs.foto, docs.notas, docs.plan]
    elif datocargado == "titulouniversitario":
        formulariodocs = [user.pk, docs.tituloeducacion, True,
                          docs.identificacion, docs.foto, docs.notas, docs.plan]
    elif datocargado == "identificacion":
        formulariodocs = [user.pk, docs.tituloeducacion, docs.titulouniversitario,
                          True, docs.foto, docs.notas, docs.plan]
    elif datocargado == "fotoperfil":
        formulariodocs = [user.pk, docs.tituloeducacion, docs.titulouniversitario,
                          docs.identificacion, True, docs.notas, docs.plan]
    elif datocargado == "record_academico":
        formulariodocs = [user.pk, docs.tituloeducacion, docs.titulouniversitario,
                          docs.identificacion, docs.foto, True, docs.plan]
    elif datocargado == "plan_estudio":
        formulariodocs = [user.pk, docs.tituloeducacion, docs.titulouniversitario,
                          docs.identificacion, docs.foto, docs.notas, True]
        
    save = save_profile_processes.update_documents(request, formulariodata, formulariodocs)
    
    if save:
        del request.session['urls']
        del request.session['urlsContent']
        del request.session['urlsContentType']
        return redirect(request.META.get('HTTP_REFERER'))

def enviar_archivo_a_odoo(request, id, status):
    if request.method == 'POST':
        user = request.user
        
        convalidacion = request.POST.get('convalidacion')
        asesor = request.POST.get('asesor')
        if convalidacion == '':
            files = {
                'convalidacion': 1,
                'foto': request.FILES.get('fotoperfil'),
                'titulo':request.FILES.get('titulobachillerto'),
                'identificacion': request.FILES.get('cedulafotografia'),
                'certificacion': request.FILES.get('certificacionnotas'),
                'plan': request.FILES.get('planestudio')
            }
        else:
            files = {
                'convalidacion': 0,
                'foto': request.FILES.get('fotoperfil'),
                'titulo':request.FILES.get('titulobachillerto'),
                'identificacion': request.FILES.get('cedulafotografia')
            }
            
        files_updated = dspace_processes.name_standardization(request, files)
        
        save_data_dspace = dspace_processes.dspace_first_admission(request, files_updated)
        
        if save_data_dspace is not None:
            if convalidacion == '':
                formulariodata = [1, True,'Formulario Enviado Satisfactoriamente', user.pk]
                formulariodocumentos = [user.pk, False, False, True, True, True, True]
            else:
                formulariodata = [1, False,'Formulario Enviado Satisfactoriamente', user.pk]
                formulariodocumentos = [user.pk, True, False, True, True, False, False]
                save_data_dspace.append('N/A')
                save_data_dspace.append('N/A')
                
            save_data_dspace.append(request.POST.get('colegio_select'))
            save_data_dspace.append(request.POST.get('mi_select'))
            if asesor == '':
                save_data_dspace.append(request.POST.get('asesor_select'))
            else:
                save_data_dspace.append('Asesor')
            
            save_odoo = enviar_data_odoo(request, save_data_dspace)
            
            save = save_profile_processes.save_documents(request, formulariodata, formulariodocumentos)

            if save and save_odoo:
                data_urls = [save_data_dspace[0], save_data_dspace[1], save_data_dspace[2], save_data_dspace[3],
                             save_data_dspace[4], save_data_dspace[5]]
                insert_urls(request,data_urls)
                return revision_formulario (request, id, status)
    
class HorarioEstudianteView(LoginRequiredMixin):
    context_object_name = 'horarioEstudiante'
    template_name = 'Dashboard/Estudiante/horarioEstudiante.html'

    def horario_view(request, id, status):
        user = request.user
        url = 'https://mocki.io/v1/3c90bcb7-ee79-4d40-9944-cea729cac4ea'
        response = requests.get(url)
        data = json.loads(response.text)
        auxHora = {}
        for curso in data:
            for horario in curso['horarios']:
                if 'horario' in horario:
                    aux = horario['horario']['horaInicio']
                    dia = horario['horario']['dia']
                    hora = horario['horario']['horaInicio'] + ':' + horario['horario']['minutosInicio'] + \
                        ' - ' + horario['horario']['horaFin'] + \
                        ':' + horario['horario']['minutoFin']
                    if aux in auxHora:
                        auxHora[aux]['horario'][dia] = hora
                    else:
                        auxHora[aux] = {'curso': curso['curso'],
                            'horario': {dia: hora}}
                                      
            if 'horarioL' in horario:
                aux = horario['horarioL']['horaInicio']
                dia = horario['horarioL']['dia']
                hora = horario['horarioL']['horaInicio'] + ':' + horario['horarioL']['minutosInicio'] + \
                    ' - ' + horario['horarioL']['horaFin'] + \
                    ':' + horario['horarioL']['minutoFin']
                if aux in auxHora:
                    auxHora[aux]['horario'][dia] = hora
                else:
                    auxHora[aux] = {'curso': curso['curso'],
                        'horario': {dia: hora}}
            if 'horarioR' in horario:
                aux = horario['horarioR']['horaInicio']
                dia = horario['horarioR']['dia']
                hora = horario['horarioR']['horaInicio'] + ':' + horario['horarioR']['minutosInicio'] + \
                    ' - ' + horario['horarioR']['horaFin'] + \
                    ':' + horario['horarioR']['minutoFin']
                if aux in auxHora:
                    auxHora[aux]['horario'][dia] = hora
                else:
                    auxHora[aux] = {'curso': curso['curso'],
                        'horario': {dia: hora}}
        dias = ['L', 'K', 'M', 'J', 'V', 'S']
        try:
            fotoperfil_obj = fotoperfil.objects.get(user=user.pk)
            imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))
            context = {
                'user': user,
                'fotoperfil': imagen_url,
                'status': status,
                'id': id,
                'horarios': sorted(auxHora.items()),
                'dias': dias
            }
        except fotoperfil.DoesNotExist:
            context = {
                'user': user,
                'status': status,
                'id': id,
                'horarios': sorted(auxHora.items()),
                'dias': dias
            }
        return render(request, 'Dashboard/Estudiante/horarioEstudiante.html', context)

class PlanDeEstudioView(LoginRequiredMixin, View):
    context_object_name = 'planEstudio'
    template_name = 'Dashboard/Estudiante/planEstudio.html'
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        url = 'https://mocki.io/v1/9da2b776-a811-4491-b5d9-6144abefb58c'
        response = requests.get(url)
        data = json.loads(response.text)
        try:
            fotoperfil_obj = fotoperfil.objects.get(user=user.pk)
            imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))
            context = {
                'user': user,
                'fotoperfil': imagen_url,
                'status': self.kwargs['status'],
                'id': self.kwargs['id'],
                'carrera': data
            }
        except fotoperfil.DoesNotExist:
            context = {
                'user': user,
                'status': self.kwargs['status'],
                'id': self.kwargs['id'],
                'carrera': data
            }
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

class DetallePlanDeEstudioView(LoginRequiredMixin):
    context_object_name = 'planEstudioCarrera'
    template_name = 'Dashboard/Estudiante/planEstudio.html'
    
    def getPlan(request, id, status):
        carrera = request.GET.get("carrera")
        url = 'https://mocki.io/v1/bf64c0f4-12c3-4581-8099-71e553044eda'
        response = requests.get(url)
        data = response.json()
        return JsonResponse(data, safe=False)
    
class MisCursos(LoginRequiredMixin):
    context_object_name = 'misCursos'
    template_name = 'Dashboard/Estudiante/misCursos.html'
    
    def misCursos_view(request, id, status):
        url = 'https://mocki.io/v1/9c1031b5-7858-4c9f-bd15-e38be55845f2'
        response = requests.get(url)
        data = json.loads(response.text)
        user = request.user
        try:
            fotoperfil_obj = fotoperfil.objects.get(user=user.pk)
            imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))
            context = {
                'user': user,
                'fotoperfil': imagen_url,
                'status': status,
                'id': id,
                'misCursos': data
            }
        except fotoperfil.DoesNotExist:
            context = {
                'user': user,
                'status': status,
                'id': id,
                'misCursos': data
            }
        return render(request, 'Dashboard/Estudiante/misCursos.html', context)