from django.shortcuts import render, redirect, get_object_or_404
from .models import profesor, estudiantes, RegistroLogsUser, documentos, carreras, colegios, posgrados, fotoperfil, estados, etapas, primerIngreso, prospecto
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
import threading
import requests
import json
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
import random
from django.urls import reverse
from .backends import MicrosoftGraphBackend
from django.core.cache import cache


type_user = ''
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
        # Get the user object from the form data
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user = authenticate(self.request, username=username, password=password)

        # Call the parent form_valid method if the user is not authenticated
        if user is None:
            form.add_error('username', 'El usuario no existe en el sistema')
            logout(self.request)
            return super().form_invalid(form)
        else:
            registrar_accion(user, 'El usuario {0} ha ingresado como prospecto.'.format(user.username))
            global type_user
            type_user = 'prospecto'
            context = {'id': username, 'status': 3}
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
            tipo_user = MicrosoftGraphBackend.type_user(request=request, access_token=access_token)
            
            if user is not None and tipo_user is not None:
                if user.is_active:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    if tipo_user == 'Estudiante':
                        registrar_accion(user, 'El usuario {0} ha ingresado como estudiante.'.format(user.username))
                        global type_user
                        type_user = 'estudiante'
                        context = {'id': user.username, 'status': 1}
                        return redirect(reverse('estudiante', kwargs=context))
                    elif tipo_user == 'Profesores':
                        registrar_accion(user, 'El usuario {0} ha ingresado como profesor.'.format(user.username))
                        global type_user
                        type_user = 'profesor'
                        context = {'id': user.username, 'status': 2}
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
        tipo_user = MicrosoftGraphBackend.type_user(request=request, access_token=access_token)
        
        if user is not None and tipo_user is not None:
            if user.is_active:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if tipo_user == 'Estudiante':
                    registrar_accion(user, 'El usuario {0} ha ingresado como estudiante.'.format(user.username))
                    context = {'id': user.username, 'status': 1}
                    return redirect(reverse('estudiante', kwargs=context))
                elif tipo_user == 'Profesores':
                    registrar_accion(user, 'El usuario {0} ha ingresado como profesor.'.format(user.username))
                    context = {'id': user.username, 'status': 2}
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
        sexo = self.request.POST.get('Genero_select')

        datos_estudiante = [username, nombre_estudiante, primerapellido,
            segundoapellido, fecha, telefono, telefono2, 'No Asignado', correo_personal, nacionalidad, provincia, canton, distrito, sexo]

        form = FormularioProspecto({'identificacion': datos_estudiante[0], 'nombre': datos_estudiante[1], 'primer_apellido': datos_estudiante[2],
                'segundo_apellido': datos_estudiante[3], 'fecha_nacimiento': datos_estudiante[4], 'numero_telefonico': datos_estudiante[5], 'numero_telefonico2': datos_estudiante[6],
                'correo_institucional': datos_estudiante[7], 'correo_personal': datos_estudiante[8], 'nacionalidad': datos_estudiante[9], 'provincia': datos_estudiante[10],
                'canton': datos_estudiante[11], 'distrito': datos_estudiante[12], 'sexo': datos_estudiante[13]})
            
        if form.is_valid():
            form.save()
        
        user = User.objects.get(username=username)
        
        if user is not None:
            
            subject = 'Se ha creado su cuenta satisfactoriamente'
            message = f'Bienvenido al portal academico UIA, su cuenta se ha creado satisfactoriamente con el usuario {user.username}, Saludos cordiales.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            
            login(self.request, user)
            
            registrar_accion(user, 'El usuario ' + username +
                             ' se ha creado una cuenta como prospecto.')
            
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


class CrearUsuario(LoginRequiredMixin, CreateView):
    fields = ['nombre', 'primer_apellido',
              'segundo_apellido', 'segundo_apellido']
    success_url = reverse_lazy('usuario')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearUsuario, self).form_valid(form)


def obtener_datos(request):
    id = request.GET.get("identificacion")
    url = 'https://api.hacienda.go.cr/fe/ae?identificacion=' + id
    response = requests.get(url)

    data_usuario = json.loads(response.text)

    if len(id) == 9:
        data_nombre = data_usuario["nombre"]
        if data_nombre is not None:
            nombre_completo = data_nombre.split()

            nombre = ' '.join(nombre_completo[:-2]).title()
            primer_apellido = nombre_completo[-2].title()
            segundo_apellido = nombre_completo[-1].title()

            data = [nombre, primer_apellido, segundo_apellido]
        else:
            data = []

    elif len(id) >= 10 and len(id) <= 12:
        data_nombre = data_usuario["nombre"]
        if data_nombre is not None:
            data = ['Existe']
        else:
            data = []
    else:
        data = []

    data_completa = json.dumps(data)
    return JsonResponse(data_completa, safe=False)


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


def guardar_perfil(request):
    if request.method == 'POST':
        user = request.user
        numero_telefonico = request.POST.get('numero_telefonico')
        numero_telefonico2 = request.POST.get('numero_telefonico2')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        distrito = request.POST.get('distrito')

        user = User.objects.get(username=user.username)
    
        if type_user == 'profesor' or type_user == 'estudiante':
            estudiante = get_object_or_404(estudiantes, identificacion=user.username)
            
            if estudiante is not None:
                datos_estudiante = [estudiante.identificacion, estudiante.nombre, estudiante.primer_apellido,
                                estudiante.segundo_apellido, estudiante.fecha_nacimiento, numero_telefonico, numero_telefonico2, estudiante.correo_institucional, estudiante.correo_personal, estudiante.nacionalidad, provincia, canton, distrito, estudiante.sexo]

                form = FormularioEstudiantes({'identificacion': datos_estudiante[0], 'nombre': datos_estudiante[1], 'primer_apellido': datos_estudiante[2],
                                            'segundo_apellido': datos_estudiante[3], 'fecha_nacimiento': datos_estudiante[4], 'numero_telefonico': datos_estudiante[5], 'numero_telefonico2': datos_estudiante[6],
                                            'correo_institucional': datos_estudiante[7], 'correo_personal': datos_estudiante[8], 'nacionalidad': datos_estudiante[9], 'provincia': datos_estudiante[10],
                                            'canton': datos_estudiante[11], 'distrito': datos_estudiante[12], 'sexo': datos_estudiante[13]}, instance=estudiante)

                if form.is_valid():
                    form.save()
                    
            profesores = get_object_or_404(profesor, identificacion=user.username)
            
            if profesores is not None:
                datos_profesor = [profesores.identificacion, profesores.nombre, profesores.primer_apellido,
                              profesores.segundo_apellido, profesores.fecha_nacimiento, numero_telefonico, numero_telefonico2, profesores.correo_institucional, profesores.correo_personal, profesores.nacionalidad, provincia, canton, distrito, profesores.sexo, profesores.puesto_educativo]

                form = FormularioProfesor({'identificacion': datos_profesor[0], 'nombre': datos_profesor[1], 'primer_apellido': datos_profesor[2],
                                        'segundo_apellido': datos_profesor[3], 'fecha_nacimiento': datos_profesor[4], 'numero_telefonico': datos_profesor[5], 'numero_telefonico2': datos_profesor[6],
                                        'correo_institucional': datos_profesor[7], 'correo_personal': datos_profesor[8], 'nacionalidad': datos_profesor[9], 'provincia': datos_profesor[10],
                                        'canton': datos_profesor[11], 'distrito': datos_profesor[12], 'sexo': datos_profesor[13], 'puesto_educativo': datos_profesor[14]}, instance=profesores)
                if form.is_valid():
                    form.save()

            return redirect(request.META.get('HTTP_REFERER'))

        elif type_user == 'profesor' or type_user == 'prospecto':
            estudiante = get_object_or_404(
                prospecto, identificacion=user.username)
            
            if estudiante is not None:
                datos_estudiante = [estudiante.user, estudiante.identificacion, estudiante.nombre, estudiante.primer_apellido,
                                    estudiante.segundo_apellido, estudiante.fecha_nacimiento, numero_telefonico, numero_telefonico2, estudiante.correo_institucional,
                                    estudiante.correo_personal, estudiante.nacionalidad, provincia, canton, distrito, estudiante.sexo]

                form = FormularioProspecto({'user': datos_estudiante[0], 'identificacion': datos_estudiante[1], 'nombre': datos_estudiante[2], 'primer_apellido': datos_estudiante[3],
                                            'segundo_apellido': datos_estudiante[4], 'fecha_nacimiento': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6], 'numero_telefonico2': datos_estudiante[7],
                                            'correo_institucional': datos_estudiante[8], 'correo_personal': datos_estudiante[9], 'nacionalidad': datos_estudiante[10], 'provincia': datos_estudiante[11],
                                            'canton': datos_estudiante[12], 'distrito': datos_estudiante[13], 'sexo': datos_estudiante[14]}, instance=estudiante)

                if form.is_valid():
                    form.save()
                
                
            profesores = get_object_or_404(profesor, identificacion=user.username)

            if profesores is not None:
                datos_profesor = [profesores.identificacion, profesores.nombre, profesores.primer_apellido,
                                profesores.segundo_apellido, profesores.fecha_nacimiento, numero_telefonico, numero_telefonico2, profesores.correo_institucional, profesores.correo_personal, profesores.nacionalidad, provincia, canton, distrito, profesores.sexo, profesores.puesto_educativo]

                form = FormularioProfesor({'identificacion': datos_profesor[0], 'nombre': datos_profesor[1], 'primer_apellido': datos_profesor[2],
                                        'segundo_apellido': datos_profesor[3], 'fecha_nacimiento': datos_profesor[4], 'numero_telefonico': datos_profesor[5], 'numero_telefonico2': datos_profesor[6],
                                        'correo_institucional': datos_profesor[7], 'correo_personal': datos_profesor[8], 'nacionalidad': datos_profesor[9], 'provincia': datos_profesor[10],
                                        'canton': datos_profesor[11], 'distrito': datos_profesor[12], 'sexo': datos_profesor[13], 'puesto_educativo': datos_profesor[14]}, instance=profesores)
                if form.is_valid():
                    form.save()
                    
            return redirect(request.META.get('HTTP_REFERER'))

        if form.is_valid():
            form.save()

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


lock = threading.Lock()


class SessionTimeoutView(LoginRequiredMixin):
    template_name = 'usuarios/login.html'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        print("Dispatching to session timeout view...")
        logout(request)
        return super().dispatch(request, *args, **kwargs)


def obtener_provincia(request):
    url = 'https://ubicaciones.paginasweb.cr/provincias.json'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def obtener_canton(request):
    id = request.GET.get("provincia_select")
    url = 'https://ubicaciones.paginasweb.cr/provincia/'+id+'/cantones.json'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def obtener_distrito(request):
    id_provincia = request.GET.get("provincia_select")
    id_canton = request.GET.get("canton_select")
    url = 'https://ubicaciones.paginasweb.cr/provincia/' +id_provincia+'/canton/'+id_canton+'/distritos.json'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data, safe=False)


def obtener_nacionalidad(request):
    url = 'https://restcountries.com/v3.1/all?fields=name'
    response = requests.get(url)
    data = response.json()
    countries = []
    for country in data:
        countries.append(country["name"]["common"])
    return JsonResponse(sorted(countries), safe=False)


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


def sesion_expirada(request):
    return render(request, 'sesion_expirada.html')


def change_email(request):
    codigo = random.randint(100000, 999999)

    user = request.user
    subject = 'Cambio de Correo Electronico'
    message = f'Hola, {user.username}, se ha solicitado modificar el correo electronico personal.\n\nEl código es: {codigo}\n\nEL CODIGO SOLO ES VALIDO PARA EL DIA DE HOY.\n\nUn cordial saludo.\nUIA.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]

    send_mail(subject, message, email_from, recipient_list)

    return render(request, 'usuario/cambio_correo_codigo.html', {'codigo': codigo})


def change_email_correct(request):
    if request.method == 'POST':
        user = request.user

        nuevo_correo = request.POST.get('nuevo_correo2')

        user = User.objects.get(username=user.username)

        estudiante = get_object_or_404(prospecto, identificacion=user.username)

        datos_estudiante = [estudiante.user, estudiante.identificacion, estudiante.nombre, estudiante.primer_apellido,
                            estudiante.segundo_apellido, estudiante.fecha_nacimiento, estudiante.numero_telefonico, estudiante.numero_telefonico2, estudiante.correo_institucional,
                            nuevo_correo, estudiante.nacionalidad, estudiante.provincia, estudiante.canton, estudiante.distrito, estudiante.sexo]

        form = FormularioProspecto({'user': datos_estudiante[0], 'identificacion': datos_estudiante[1], 'nombre': datos_estudiante[2], 'primer_apellido': datos_estudiante[3],
                                    'segundo_apellido': datos_estudiante[4], 'fecha_nacimiento': datos_estudiante[5], 'numero_telefonico': datos_estudiante[6], 'numero_telefonico2': datos_estudiante[7],
                                    'correo_institucional': datos_estudiante[8], 'correo_personal': datos_estudiante[9], 'nacionalidad': datos_estudiante[10], 'provincia': datos_estudiante[11],
                                    'canton': datos_estudiante[12], 'distrito': datos_estudiante[13], 'sexo': datos_estudiante[14]}, instance=estudiante)

        if form.is_valid():
            form.save()
            # hola Victor
            return redirect('perfil_prospecto')


def revision_formulario(request, id, status):
    user = request.user

    # Obtener el objeto de la base de datos según su ID
    statusgeneral = get_object_or_404(primerIngreso, usuario=user.pk)

    etapa = get_object_or_404(etapas, id_etapa=statusgeneral.etapa_id)

    estado = get_object_or_404(estados, id_estado=statusgeneral.estado_id)

    docs = get_object_or_404(documentos, usuario=user.pk)

    fotoperfil_obj = fotoperfil.objects.get(user=user.pk)
    imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))

    # Enviar el objeto y otros datos necesarios a la plantilla HTML
    contexto = {
        "fotoperfil": imagen_url,
        "comentario": statusgeneral.comentario,
        "etapa": etapa.etapa_nombre,
        "estado": estado.estado_nombre,
        "convalidacion": statusgeneral.convalidacion,
        "documentos": docs,
        "id": id,
        "status": status,
    }
    return render(request, "Dashboard/Prospecto/revision_form.html", contexto)


def corregirdata(request):
    user = request.user

    datocargado = request.POST.get('documentocargado')

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

    form = FormularioPrimerIngreso({'etapa': formulariodata[0], 'estado': formulariodata[1], 'convalidacion': formulariodata[2],
                                    'usuario': formulariodata[3], 'comentario': formulariodata[4]}, instance=statusgeneral)
    if form.is_valid():
        form.save()

    if datocargado == "titulo":
        formulariodocs = [user.pk, True, docs.titulouniversitario,
                          docs.identificacion, docs.foto, docs.notas, docs.plan]
    elif datocargado == "titulouniversitario":
        formulariodocs = [user.pk, docs.tituloeducacion, True,
                          docs.identificacion, docs.foto, docs.notas, docs.plan]
    elif datocargado == "identificacion":
        formulariodocs = [user.pk, docs.tituloeducacion, docs.titulouniversitario,
                          True, docs.foto, docs.notas, docs.plan]
    elif datocargado == "foto":
        formulariodocs = [user.pk, docs.tituloeducacion, docs.titulouniversitario,
                          docs.identificacion, True, docs.notas, docs.plan]
    elif datocargado == "notas":
        formulariodocs = [user.pk, docs.tituloeducacion, docs.titulouniversitario,
                          docs.identificacion, docs.foto, True, docs.plan]
    elif datocargado == "plan":
        formulariodocs = [user.pk, docs.tituloeducacion, docs.titulouniversitario,
                          docs.identificacion, docs.foto, docs.notas, True]

    form = FormularioDocumentos({'usuario': formulariodocs[0], 'tituloeducacion': formulariodocs[1],
                                 'titulouniversitario': formulariodocs[2], 'identificacion': formulariodocs[3],
                                 'foto': formulariodocs[4], 'notas': formulariodocs[5],
                                 'plan': formulariodocs[6]}, instance=docs)

    if form.is_valid():
        form.save()
        return redirect(request.META.get('HTTP_REFERER'))


def autenticacion():
    # DSPACE ACTIONS
    session = requests.Session()

    # Obtener el token CSRF
    csrf_url = 'http://dspace.uia.ac.cr:8080/server/api/authn'
    csrf_response = session.get(csrf_url)
    if csrf_response.status_code == 200:
        csrf_token = csrf_response.cookies.get('DSPACE-XSRF-COOKIE')
        print('Token de CSRF:', csrf_token)
    else:
        print('Error al obtener el token de CSRF')


def enviar_archivo_a_odoo(request, id, status):
    if request.method == 'POST':
        user = request.user
        user_id = user.pk
        estudiante = get_object_or_404(usuarios, auth_user=user_id)
        # foto = request.FILES.get('fotoperfil')

        # img_data = foto.read()

        # # Convertir la imagen a bytes
        # img_bytes = bytearray(img_data)

        # # Crear el objeto UserFile y guardarlo en la base de datos
        # user_file = fotoperfil(user=estudiante, archivo=img_bytes)
        # user_file.save()

        # usuario = get_object_or_404(usuarios, auth_user=user_id)
        # formulariodata = [1, 1, False, usuario.pk,'Formulario Enviado Satisfactoriamente']

        # form = FormularioPrimerIngreso({ 'etapa': formulariodata[0], 'estado': formulariodata[1], 'convalidacion': formulariodata[2],
        #                                 'usuario': formulariodata[3],'comentario': formulariodata[4]})
        # if form.is_valid():
        #     form.save()

        # formulariodocumentos = [usuario.pk, True, False, True, True, True, True]

        # form = FormularioDocumentos({'usuario': formulariodocumentos[0], 'tituloeducacion': formulariodocumentos[1],
        #                              'titulouniversitario': formulariodocumentos[2], 'identificacion': formulariodocumentos[3],
        #                              'foto': formulariodocumentos[4], 'notas': formulariodocumentos[5],
        #                              'plan': formulariodocumentos[6]})

        # if form.is_valid():
        #     form.save()
        #     context = {'id': id, 'status': status}

        # DSPACE ACTIONS
        session = requests.Session()

        # Obtener el token CSRF
        csrf_url = 'http://dspace.uia.ac.cr:8080/server/api/authn'
        csrf_response = session.get(csrf_url)
        if csrf_response.status_code == 200:
            csrf_token = csrf_response.cookies.get('DSPACE-XSRF-COOKIE')
            print('Token de CSRF:', csrf_token)
        else:
            print('Error al obtener el token de CSRF')

        # Autenticarse con DSpace utilizando el token CSRF
        auth_url = 'http://dspace.uia.ac.cr:8080/server/api/authn/login'
        username = 'pruebas_dspace@uia.ac.cr'
        password = 'God69061'
        data = {"user": username, "password": password}
        headers = {"X-XSRF-TOKEN": csrf_token}
        response = session.post(auth_url, data=data, headers=headers)

        if response.status_code == 200:
            token = response.headers.get('Authorization')
            csrf_token_login = response.cookies.get('DSPACE-XSRF-COOKIE')
            print('Token de autenticación:', token)
        else:
            print('Error de autenticación')

        # Obtener el ID de la comunidad
        community_name = "Academia UIA"
        community_url = "http://dspace.uia.ac.cr:8080/server/api/core/communities"
        response = session.get(community_url, headers=headers)
        communities = json.loads(response.text)
        community_id = ""
        for community in communities['_embedded']['communities']:
            if community['name'] == community_name:
                community_id = community['uuid']
                break

        # Obtener el ID de la colección
        collection_name = "PRIMER INGRESO"
        collection_url = "http://dspace.uia.ac.cr:8080/server/api/core/communities/" +community_id+"/collections"
        response = session.get(collection_url, headers=headers)
        collections = json.loads(response.text)
        collection_id = ""
        for collection in collections['_embedded']['collections']:
            if collection['name'] == collection_name:
                collection_id = collection['uuid']
                break

        file = request.FILES['titulobachillerto']
        file_name = file.name

        # Crear el objeto de carga de archivo
        files  = [('file', (file.name, file.read(), file.content_type))]
        
        headers = {  
            "Authorization": token,           
            "X-XSRF-TOKEN": csrf_token_login,
        }
        
        bundle = {
            "name": "PRIMER_INGRESO",
            "metadata": {
            },
        }
        
        data = {
            f'properties': '{ "name": "'+file_name+'", "metadata": { "dc.description": [ { "value": "example file", "language": null, "authority": null, "confidence": -1, "place": 0 }]}, "bundleName": "PRIMER_INGRESO" }'
        }
        
        payload = data
        
        item_id = "b3994898-55fd-4a3b-8c51-8e22a8ec847d"
        
        bundle_id = "ca6a6a08-657e-4356-8833-1b0699b1c279"
        
        bundle_id2 = "79774be9-f1b8-47cc-994f-497f9b572990"
        
        upload_url = "http://dspace.uia.ac.cr:8080/server/api/core/bundles/"+bundle_id2+"/bitstreams"
        
        response = session.post(upload_url, headers=headers, data=data, files=files)
        
        if response.status_code == 201:
            print('Archivo enviado con éxito')
            bitstream_id = response.json()
            print('URL del archivo:', bitstream_id)
            
            url_asociar_bitstream = "http://dspace.uia.ac.cr:8080/server/api/core/items/"+item_id+"/bitstreams?name="+file_name
        
            response = session.put(url_asociar_bitstream, headers=headers, files=properties_data, data=data)
            
            if response.status_code == 200:
                print("Archivo cargado con éxito en DSpace.")
            else:
                print("Se produjo un error al cargar el archivo en DSpace.")
        else:
            print('Error al enviar el archivo')

        # Cierre de sesión
        logout_url = 'http://dspace.uia.ac.cr:8080/server/api/authn/logout'

        response = session.post(logout_url, headers=headers)

        if response.status_code == 204:
            print('Sesión cerrada exitosamente')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            print('Error al cerrar la sesión')