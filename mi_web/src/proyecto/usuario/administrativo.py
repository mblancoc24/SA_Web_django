from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
import base64
import datetime
from datetime import time
from django.contrib.auth.models import User, Group
import json
import pytz

from usuario.api_queries import get_professor, get_student
from .models import imagenNoticia, noticias, RegistroLogsUser, prospecto
import requests
from django.core.mail import send_mail
from django.conf import settings

def registrar_accion(usuario, accion):
    registro = RegistroLogsUser(usuario=usuario, accion=accion)
    registro.save()

class DashboardAdministrativoView(LoginRequiredMixin, View):
    context_object_name = 'inicioAdministrativo'
    def get(self, request,type, id, status):
        context = {
                'type': type,
                'id': id,
                'status': status,
            }
        if type == "administrador" and id == 'mercadeo':
            context['fotoNoticia'] = ImagenNoticias.mostrarFotosNoticias('')
            context['Noticias'] = Noticias.mostrarNoticias('')
            return render(request, 'Dashboard/Administrativo/Mercadeo/mercadeo.html', context)
        elif type == "administrador" and id == 'soporte':
            context['usuariosE'] = userGroup('Estudiante')
            context['usuariosP'] = userGroup('Profesor')
            context['usuariosPr'] = userGroup('Prospecto')
            context['usuariosH'] = historialAccion()
            return render(request, 'Dashboard/Administrativo/Soporte/soporte.html', context)
    
class ImagenNoticias(LoginRequiredMixin, View):

    def guardarImagenNoticia(request):
        imgnueva = request.FILES.get('imagen')
        fechaI = request.POST.get('fechaI')
        horaI = request.POST.get('horaI')
        fechaF = request.POST.get('fechaF')
        horaF = request.POST.get('horaF')
        tipo = request.POST.get('tipo')
        tipoE = request.POST.get('tipoE')
        tipoP = request.POST.get('tipoP')
        tipoE = tipoE.lower() == 'true'
        tipoP = tipoP.lower() == 'true'
        user = request.user

        if request.method == 'POST':
            try:
                if imgnueva is not None:
                    img_data = imgnueva.read()
                    img_bytes = bytearray(img_data)
                    nombre_archivo = imgnueva.name
                    fotoNoticia = imagenNoticia(imagen=img_bytes, imagen_nombre=nombre_archivo, estudiante=tipoE, profesor=tipoP,fecha_inicio=fechaI,fecha_fin=fechaF,hora_inicio=horaI,hora_fin=horaF)
                    fotoNoticia.save()
                    registrar_accion(user, 'El usuario {0} ha guardado una imagen de noticia para {1}'.format(user.username, tipo))
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'error': str(e)})
    
    def mostrarFotosNoticias(id):
        if id == 'estudiante':
            fotos = imagenNoticia.objects.filter(estudiante=True)
        elif id == 'profesor':
            fotos = imagenNoticia.objects.filter(profesor=True)
        else:
            fotos = imagenNoticia.objects.all()
        imagenes = []
        for foto in fotos:
            fechaI_formateada = foto.fecha_inicio.strftime("%Y-%m-%d")
            fechaF_formateada = foto.fecha_fin.strftime("%Y-%m-%d")
            hora_inicio_formateada = foto.hora_inicio.strftime("%H:%M")
            hora_fin_formateada = foto.hora_fin.strftime("%H:%M")
            imagen_dict = {
                'id': foto.id,
                'imagen': base64.b64encode(bytes(foto.imagen)).decode('utf-8'),
                'imagen_nombre': foto.imagen_nombre,
                'fecha_inicio': fechaI_formateada,
                'fecha_fin' : fechaF_formateada,
                'hora_inicio': hora_inicio_formateada,
                'hora_fin': hora_fin_formateada,
                'estudiante': foto.estudiante,
                'profesor': foto.profesor,
            }
            imagenes.append(imagen_dict)
        return imagenes
    
    def mostrarFotosNoticiasU(request, id):
        ajax = request.GET.get("flag")
        context = {}
        fotosAux = request.session.get('publicidad')
        if fotosAux is None:
            if id == 'estudiante':
                fotos = imagenNoticia.objects.filter(estudiante=True)
            elif id == 'profesor':
                fotos = imagenNoticia.objects.filter(profesor=True)
                
        else:
            eventos_seleccionadosE = []
            if ajax is None:
                ajax = False
            if ajax and id == 'estudiante':
                for evento in filtro(request, 'publicidad'):
                    eventos_seleccionadosE.append(evento)
                context['imagenes_estudiante'] = eventos_seleccionadosE
                return JsonResponse(context, safe=False)
            elif ajax and id == 'profesor':
                for evento in filtro(request, 'publicidad'):
                    eventos_seleccionadosE.append(evento)
                context['imagenes_profesor'] = eventos_seleccionadosE
                return JsonResponse(context, safe=False)
            else:
                for evento in filtro(request, 'publicidad'):
                    eventos_seleccionadosE.append(evento)
                return eventos_seleccionadosE
        imagenes = []
        for foto in fotos:
            fechaI_formateada = foto.fecha_inicio.strftime("%Y-%m-%d")
            fechaF_formateada = foto.fecha_fin.strftime("%Y-%m-%d")
            hora_inicio_formateada = foto.hora_inicio.strftime("%H:%M")
            hora_fin_formateada = foto.hora_fin.strftime("%H:%M")
            imagen_dict = {
                'id': foto.id,
                'imagen': base64.b64encode(bytes(foto.imagen)).decode('utf-8'),
                'imagen_nombre': foto.imagen_nombre,
                'fecha_inicio': fechaI_formateada,
                'fecha_fin' : fechaF_formateada,
                'hora_inicio': hora_inicio_formateada,
                'hora_fin': hora_fin_formateada,
                'estudiante': foto.estudiante,
                'profesor': foto.profesor,
            }
            imagenes.append(imagen_dict)

        eventos_seleccionados = []
        
        request.session['publicidad'] = imagenes
        for evento in filtro(request, 'publicidad'):
            eventos_seleccionados.append(evento)
        if ajax is None:
            ajax = False
        if ajax and id == 'estudiante':
            context['imagenes_estudiante'] = eventos_seleccionados
            return JsonResponse(context, safe=False)
        elif ajax and id == 'profesor':
            context['imagenes_profesor'] = eventos_seleccionados
            return JsonResponse(context, safe=False)
        else:
            return eventos_seleccionados
        
    def borrarFotosNoticias(request):
        user = request.user
        if request.method == 'POST':
            try:
                id = request.POST.get("id")
                imagen_noticia = imagenNoticia.objects.get(id=id)
                registrar_accion(user, 'El usuario {0} ha borrado una imagen de noticia'.format(user.username))
                imagen_noticia.delete()
                return JsonResponse({'success': True})
            except imagenNoticia.DoesNotExist:
                return JsonResponse({'success': False})
            except Exception as e:
                return JsonResponse({'error': str(e)})
    
    def mostrarFotosNoticiasId(request):
        if request.method == 'GET':
            try:
                id = request.GET.get("id")
                imagen_noticia = imagenNoticia.objects.get(id=id)
                imagenes = []
                imagen_dict = {
                        'id': imagen_noticia.id,
                        'imagen': base64.b64encode(bytes(imagen_noticia.imagen)).decode('utf-8'),
                        'imagen_nombre': imagen_noticia.imagen_nombre,
                        'fecha_inicio': imagen_noticia.fecha_inicio,
                        'fecha_fin' : imagen_noticia.fecha_fin,
                        'hora_inicio': imagen_noticia.hora_inicio,
                        'hora_fin': imagen_noticia.hora_fin,
                        'estudiante': imagen_noticia.estudiante,
                        'profesor': imagen_noticia.profesor,
                    }
                imagenes.append(imagen_dict)
                context = {'fotoNoticia': imagenes}
                return JsonResponse(context, safe=False)
            except imagenNoticia.DoesNotExist:
                return JsonResponse({'error': 'La imagen de noticia no existe.'})
            except Exception as e:
                return JsonResponse({'error': str(e)})
            
    def actualizarFotosNoticias(request):
        imgnueva = request.FILES.get('imagen')
        user = request.user
        fechaI = request.POST.get('fechaI')
        horaI = request.POST.get('horaI')
        fechaF = request.POST.get('fechaF')
        horaF = request.POST.get('horaF')
        tipo = request.POST.get('tipo')
        tipoE = request.POST.get('tipoE')
        tipoP = request.POST.get('tipoP')
        tipoE = tipoE.lower() == 'true'
        tipoP = tipoP.lower() == 'true'
        if request.method == 'POST':
            try:
                id = request.POST.get("id")
                imagen_noticia = imagenNoticia.objects.get(id=id)
                if imgnueva is not None:
                    img_data = imgnueva.read()
                    img_bytes = bytearray(img_data)
                    nombre_archivo = imgnueva.name
                    imagen_noticia.imagen = img_bytes
                    imagen_noticia.imagen_nombre = nombre_archivo
                    imagen_noticia.estudiante = tipoE
                    imagen_noticia.profesor = tipoP
                    imagen_noticia.fecha_inicio = fechaI
                    imagen_noticia.fecha_fin = fechaF
                    imagen_noticia.hora_inicio = horaI
                    imagen_noticia.hora_fin = horaF
                    imagen_noticia.save()
                    registrar_accion(user, 'El usuario {0} ha actualizado una imagen de noticia para {1}'.format(user.username, tipo))
                    return JsonResponse({'success': True})
                else:
                    imagen_noticia.estudiante = tipoE
                    imagen_noticia.profesor = tipoP
                    imagen_noticia.fecha_inicio = fechaI
                    imagen_noticia.fecha_fin = fechaF
                    imagen_noticia.hora_inicio = horaI
                    imagen_noticia.hora_fin = horaF
                    imagen_noticia.save()
                    registrar_accion(user, 'El usuario {0} ha actualizado una imagen de noticia para {1}'.format(user.username, tipo))
                    return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False})

class Noticias(LoginRequiredMixin, View):
    
    def guardarNoticia(request):
        imgnueva = request.FILES.get('imagen')
        tituloN = request.POST.get('titulo')
        descripcionN = request.POST.get('descripcion')
        fechaI = request.POST.get('fechaI')
        horaI = request.POST.get('horaI')
        fechaF = request.POST.get('fechaF')
        horaF = request.POST.get('horaF')
        tipo = request.POST.get('tipo')
        tipoE = request.POST.get('tipoE')
        tipoP = request.POST.get('tipoP')
        tipoE = tipoE.lower() == 'true'
        tipoP = tipoP.lower() == 'true'
        user = request.user
        if request.method == 'POST':
            try:
                if imgnueva is not None:
                    img_data = imgnueva.read()
                    img_bytes = bytearray(img_data)
                    nombre_archivo = imgnueva.name
                    noticia = noticias(imagen=img_bytes, imagen_nombre=nombre_archivo, titulo=tituloN, descripcion=descripcionN, estudiante=tipoE, profesor=tipoP,fecha_inicio=fechaI,fecha_fin=fechaF,hora_inicio=horaI,hora_fin=horaF)
                    noticia.save()
                    registrar_accion(user, 'El usuario {0} ha guardado una noticia para {1}'.format(user.username, tipo))
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'error': str(e)})
            
    def mostrarNoticias(id):
        if id == 'estudiante':
            noticiaList = noticias.objects.filter(estudiante=True)
        elif id == 'profesor':
            noticiaList = noticias.objects.filter(profesor=True)
        else:
            noticiaList = noticias.objects.all()
        noticiasList = []
        for noticia in noticiaList:
            fechaI_formateada = noticia.fecha_inicio.strftime("%Y-%m-%d")
            fechaF_formateada = noticia.fecha_fin.strftime("%Y-%m-%d")
            hora_inicio_formateada = noticia.hora_inicio.strftime("%H:%M")
            hora_fin_formateada = noticia.hora_fin.strftime("%H:%M")
            noticia_dict = {
                'id': noticia.id,
                'imagen': base64.b64encode(bytes(noticia.imagen)).decode('utf-8'),
                'imagen_nombre': noticia.imagen_nombre,
                'titulo': noticia.titulo,
                'descripcion': noticia.descripcion,
                'fecha_inicio': fechaI_formateada,
                'fecha_fin' : fechaF_formateada,
                'hora_inicio': hora_inicio_formateada,
                'hora_fin': hora_fin_formateada,
                'estudiante': noticia.estudiante,
                'profesor': noticia.profesor,
            }
            noticiasList.append(noticia_dict)
        return noticiasList
    
    def mostrarNoticiasU(request,id):
        ajax = request.GET.get("flag")
        context = {}
        fotosAux = request.session.get('noticia')
        if fotosAux is None:
            if id == 'estudiante':
                noticiaList = noticias.objects.filter(estudiante=True)
            elif id == 'profesor':
                noticiaList = noticias.objects.filter(profesor=True)
        else:
            eventos_seleccionadosN = []
            if ajax is None:
                ajax = False
            if ajax and id == 'estudiante':
                for evento in filtro(request, 'noticia'):
                    eventos_seleccionadosN.append(evento)
                context['noticia_estudiante'] = eventos_seleccionadosN
                return JsonResponse(context, safe=False)
            elif ajax and id == 'profesor':
                for evento in filtro(request, 'noticia'):
                    eventos_seleccionadosN.append(evento)
                context['noticia_profesor'] = eventos_seleccionadosN
                return JsonResponse(context, safe=False)
            else:
                for evento in filtro(request, 'noticia'):
                    eventos_seleccionadosN.append(evento)
                return eventos_seleccionadosN
                
        noticiasList = []
        for noticia in noticiaList:
            fechaI_formateada = noticia.fecha_inicio.strftime("%Y-%m-%d")
            fechaF_formateada = noticia.fecha_fin.strftime("%Y-%m-%d")
            hora_inicio_formateada = noticia.hora_inicio.strftime("%H:%M")
            hora_fin_formateada = noticia.hora_fin.strftime("%H:%M")
            noticia_dict = {
                'id': noticia.id,
                'imagen': base64.b64encode(bytes(noticia.imagen)).decode('utf-8'),
                'imagen_nombre': noticia.imagen_nombre,
                'titulo': noticia.titulo,
                'descripcion': noticia.descripcion,
                'fecha_inicio': fechaI_formateada,
                'fecha_fin' : fechaF_formateada,
                'hora_inicio': hora_inicio_formateada,
                'hora_fin': hora_fin_formateada,
                'estudiante': noticia.estudiante,
                'profesor': noticia.profesor,
            }
            noticiasList.append(noticia_dict)
        eventos_seleccionadosN = []
        request.session['noticia'] = noticiasList
        for evento in filtro(request, 'noticia'):
            eventos_seleccionadosN.append(evento)
            
        if ajax is None:
            ajax = False
        if ajax and id == 'estudiante':
            context['noticia_estudiante'] = eventos_seleccionadosN
            return JsonResponse(context, safe=False)
        elif ajax and id == 'profesor':
            context['noticia_profesor'] = eventos_seleccionadosN
            return JsonResponse(context, safe=False)
        else:
            return eventos_seleccionadosN
    
    def borrarNoticias(request):
        user = request.user
        if request.method == 'POST':
            try:
                id = request.POST.get("id")
                noticia = noticias.objects.get(id=id)
                registrar_accion(user, 'El usuario {0} ha borrado una noticia'.format(user.username))
                noticia.delete()
                return JsonResponse({'success': True})
            except imagenNoticia.DoesNotExist:
                return JsonResponse({'success': False})
            except Exception as e:
                return JsonResponse({'error': str(e)})
            
    def mostrarNoticiasId(request):
        if request.method == 'GET':
            try:
                id = request.GET.get("id")
                noticia = noticias.objects.get(id=id)
                noticiasList = []
                noticia_dict = {
                        'id': noticia.id,
                        'imagen': base64.b64encode(bytes(noticia.imagen)).decode('utf-8'),
                        'imagen_nombre': noticia.imagen_nombre,
                        'titulo': noticia.titulo,
                        'descripcion': noticia.descripcion,
                        'fecha_inicio': noticia.fecha_inicio,
                        'fecha_fin' : noticia.fecha_fin,
                        'hora_inicio': noticia.hora_inicio,
                        'hora_fin': noticia.hora_fin,
                        'estudiante': noticia.estudiante,
                        'profesor': noticia.profesor,
                    }
                noticiasList.append(noticia_dict)
                context = {'Noticias': noticiasList}
                return JsonResponse(context, safe=False)
            except imagenNoticia.DoesNotExist:
                return JsonResponse({'error': 'La noticia no existe.'})
            except Exception as e:
                return JsonResponse({'error': str(e)})
            
    def actualizarNoticias(request):
        imgnueva = request.FILES.get('imagen')
        tituloN = request.POST.get('titulo')
        descripcionN = request.POST.get('descripcion')
        fechaI = request.POST.get('fechaI')
        horaI = request.POST.get('horaI')
        fechaF = request.POST.get('fechaF')
        horaF = request.POST.get('horaF')
        tipo = request.POST.get('tipo')
        tipoE = request.POST.get('tipoE')
        tipoP = request.POST.get('tipoP')
        tipoE = tipoE.lower() == 'true'
        tipoP = tipoP.lower() == 'true'
        user = request.user
        if request.method == 'POST':
            try:
                id = request.POST.get("id")
                noticia = noticias.objects.get(id=id)
                if imgnueva is not None:
                    img_data = imgnueva.read()
                    img_bytes = bytearray(img_data)
                    nombre_archivo = imgnueva.name
                    noticia.imagen = img_bytes
                    noticia.imagen_nombre = nombre_archivo
                    noticia.titulo = tituloN
                    noticia.descripcion = descripcionN
                    noticia.estudiante = tipoE
                    noticia.profesor = tipoP
                    noticia.fecha_inicio = fechaI
                    noticia.fecha_fin = fechaF
                    noticia.hora_inicio = horaI
                    noticia.hora_fin = horaF
                    noticia.save()
                    registrar_accion(user, 'El usuario {0} ha actualizado una noticia para {1}'.format(user.username, tipo))
                    return JsonResponse({'success': True})
                else:
                    noticia.titulo = tituloN
                    noticia.descripcion = descripcionN
                    noticia.estudiante = tipoE
                    noticia.profesor = tipoP
                    noticia.fecha_inicio = fechaI
                    noticia.fecha_fin = fechaF
                    noticia.hora_inicio = horaI
                    noticia.hora_fin = horaF
                    noticia.save()
                    registrar_accion(user, 'El usuario {0} ha actualizado una noticia para {1}'.format(user.username, tipo))
                    return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False})
            
def filtro(request, id):
    eventos_seleccionados = []
    fecha_actual = datetime.date.today()
    hora_actual = datetime.datetime.now().time()
    if id == 'publicidad':
        data = request.session.get('publicidad')
    elif id == 'noticia':
        data = request.session.get('noticia')
    for evento in data:
        fecha_inicio = datetime.datetime.strptime(evento['fecha_inicio'], '%Y-%m-%d').date()
        hora_inicio = datetime.datetime.strptime(evento['hora_inicio'], '%H:%M').time()
        fecha_fin = datetime.datetime.strptime(evento['fecha_fin'], '%Y-%m-%d').date()
        hora_fin = datetime.datetime.strptime(evento['hora_fin'], '%H:%M').time()

        inicio_evento = datetime.datetime.combine(fecha_inicio, hora_inicio)
        fin_evento = datetime.datetime.combine(fecha_fin, hora_fin)
        actual = datetime.datetime.combine(fecha_actual, hora_actual)

        if inicio_evento <= actual <= fin_evento:
            eventos_seleccionados.append(evento)
    return eventos_seleccionados

def userGroup(name):
    try:
        group = Group.objects.get(name=name)
        users = group.user_set.all()
        usuariosR = []
        for usuario in users:
            user = {
            'id': usuario.username,
            'email': usuario.email,
            'fecha_creacion': usuario.date_joined.strftime("%d/%m/%Y"),
            'fecha_ingreso': usuario.last_login.strftime("%d/%m/%Y"),
            'activo': usuario. is_active,
        }
            usuariosR.append(user)
    except Group.DoesNotExist:
        usuariosR = []
    return usuariosR

def historialAccion():
    try:
        historial = RegistroLogsUser.objects.all()
        historialList = []
        for h in historial:
            usuario_email=''
            if h.usuario.email:
                usuario_email = h.usuario.email
            else:
                usuario_email = h.usuario
            timezone = pytz.timezone('America/Costa_Rica')
            fecha_local = h.fechatiempo.astimezone(timezone)
            historiaAux = {
                'usuario': usuario_email,
                'accion': h.accion,
                'fecha': fecha_local.strftime("%d/%m/%Y %H:%M:%S")
            }
            historialList.append(historiaAux)
    except RegistroLogsUser.DoesNotExist:
        historialList = []
    return historialList

class Soporte(LoginRequiredMixin, View):
    
    def getPlan(request, type, id, status):
        url = 'https://mocki.io/v1/1698cc3a-1447-45cc-bf6b-adb8e6eb3d5d'
        idEstudiante = json.dumps({'identificacion': str(604150895)})
        headers = {
            'Content-Type': 'application/json'
        }
        # response = requests.request("GET", url, headers=headers, data=idEstudiante)
        response = requests.request("GET", url)
        data = json.loads(response.text)['result']
        context = {
            'id': id,
            'status': status,
        }
        if type == 'Estudiante':
            context['carrera'] = data
            context['type'] = type
        else:
            context['type'] = type
        return render(request, 'Dashboard/Administrativo/Soporte/inspeccionarUsuario.html', context)
    
    def misCursos(request, type, id, status):
        url = 'https://mocki.io/v1/9c1031b5-7858-4c9f-bd15-e38be55845f2'
        response = requests.get(url)
        data = json.loads(response.text)
        context = {
            'id': id,
            'status': status,
        }
        if type == 'Estudiante':
            context['misCursos'] = data
            context['type'] = type
        else:
            context['type'] = type
        return render(request, 'Dashboard/Administrativo/Soporte/misCursosS.html', context)
    
    def horarios(request, type, id, status):
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
        context = {
                'status': status,
                'id': id,
            }
        if type == 'Estudiante':
            context['horarios'] = sorted(auxHora.items())
            context['dias'] = dias
            context['type'] = type
        else:
            context['type'] = type
            
        return render(request, 'Dashboard/Administrativo/Soporte/horarioS.html', context)
    
    def estadoCuenta(request, type, id, status):
        url = 'https://mocki.io/v1/0e843b73-8f53-4cf1-a191-b625e0512253'
        
        response = requests.request("GET", url)
        data = json.loads(response.text)['result']
        context = {
            'id': id,
            'status': status,
        }
        if type == 'Estudiante':
            context['financiamiento'] = data
            context['type'] = type
        else:
            context['type'] = type
        return render(request, 'Dashboard/Administrativo/Soporte/estadoCuenta.html', context)
    
    def perfil(request,type, id, status):
        user = request.user
        context = {
            'user': user,
            'id': id,
            'status': status,
        }
        if type == 'Estudiante':
            context['perfil'] = get_student(id)
            context['type'] = type
        elif type == 'Profesor':
            context['perfil'] = get_professor(id)
            context['type'] = type
        else:
            perfil = get_object_or_404(prospecto, identificacion=id)
            context['perfil'] = perfil
            context['type'] = type
        return render(request, 'Dashboard/Administrativo/Soporte/perfil.html', context)
    
    def correo(request,type, id, status):
        context = {
            'type': type,
            'id': id,
            'status': status,
        }
        return render(request, 'Dashboard/Administrativo/Soporte/correo.html', context)
    
    def sendCorreo(request):
        json_data = json.loads(request.body)
        subject = 'Reenvió de credenciales' 
        nombre = json_data.get('nombre', '')
        mensaje = json_data.get('mensaje', '') 
        correo = json_data.get('email', '') 
        recipient_list = [correo]
        context = {}
        try:
            email_credentials = settings.EMAIL_HOST_USER[1]
            email_from = email_credentials['user']
            send_mail(subject, mensaje, email_from, recipient_list, auth_user=email_credentials['user'], auth_password=email_credentials['pass'],)
            context['response'] = True
        except Exception as e:
            context['response'] = False
            context['error_message'] = str(e)
        return JsonResponse(context, safe=False)