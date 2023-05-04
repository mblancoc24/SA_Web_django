from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import profesor, estudiantes, RegistroLogsUser, documentos, carreras, colegios, posgrados, fotoperfil, estados, primerIngreso, prospecto
import json
from django.contrib.auth.models import User

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
    
def obtener_datos(request):
    id = request.GET.get("identificacion")
    if len(id) == 9:
        url = 'https://api.hacienda.go.cr/fe/ae?identificacion=' + id
        response = requests.get(url)

        data_usuario = json.loads(response.text)
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
        url = 'https://api.hacienda.go.cr/fe/ae?identificacion=' + id
        response = requests.get(url)

        data_usuario = json.loads(response.text)
        data_nombre = data_usuario["nombre"]
        if data_nombre is not None:
            data = ['Existe']
        else:
            data = []
    else:
        data = []

    data_completa = json.dumps(data)
    return JsonResponse(data_completa, safe=False)

def enviar_data_odoo(request, data):
    user = request.user
    prospecto_user = get_object_or_404(prospecto, identificacion=user.username)
    url = 'http://192.168.11.196:8062/create_prospecto'
    data = {
        "identificacion": prospecto_user.identificacion,
        "psNombre": prospecto_user.nombre,
        "primerApellido": prospecto_user.primer_apellido,
        "segundoApellido": prospecto_user.segundo_apellido,
        "colegioProcedencia": data[5],
        "carrera_id": data[6],
        "provincia": prospecto_user.provincia,
        "canton": prospecto_user.canton,
        "distrito": prospecto_user.distrito,
        "direccionExacta": prospecto_user.distrito,
        "docTitulo": data[0],
        "docIdentificacion": data[1],
        "docFotoPasaporte": data[2],
        "docMateriasAprobadas": data[3],
        "docPlanEstudios": data[4],
        "empleadoAsignadoInicial": data[7]
    }
    new_header = {  
        'Content-Type':'application/json'
    }
    
    return True
    # response = requests.post(url, headers=new_header, data=json.dumps(data))
    # result = response.json()
        
    # if response.status_code == 200:
    #     print('Sesión cerrada exitosamente')
    #     return True
    # else:
    #     print('Error al cerrar la sesión')
    #     return False
    
def get_urls_odoo(request, data):
    user = request.user
    url = 'http://192.168.11.196:8062/get_prospecto_docs'
    data = {
        'identificacion': user.username
    }
    new_header = {  
        'Content-Type':'application/json'
    }
    
    response = requests.post(url, headers=new_header, data=json.dumps(data))
    result = response.json()
        
    if response.status_code == 200:
        print('Sesión cerrada exitosamente')
        return True
    else:
        print('Error al cerrar la sesión')
        return False
