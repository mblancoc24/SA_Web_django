from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .save_processes import save_profile_processes

@csrf_exempt
def documents_status(request):
    #http://192.168.8.136:8000/documents-status/
    
    # {
    #     "data": {
    #         "id": 117580049,
    #         "estado": 2,
    #         "comentario":"Esta en revision los documentos.",
    #         "tituloeducacion": false,
    #         "titulouniversitario": true,
    #         "identificacion": true,
    #         "foto": true,
    #         "notas": true,
    #         "plan": true
    #     }
    # }
    user = request.user
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            response_data = {'error': 'Invalid JSON'}
            return JsonResponse(response_data, status=400)
            
        try:
            id_value = data['data']['id']
            status_value = data['data']['estado']
            comment = data['data']['comentario']
            
            tituloeducacion = data['data']['tituloeducacion']
            titulouniversitario = data['data']['titulouniversitario']
            identificacion = data['data']['identificacion']
            foto = data['data']['foto']
            notas = data['data']['notas']
            plan = data['data']['plan']
            
            data_status = [status_value, comment, id_value]
            
            data_documents = [id_value, tituloeducacion, titulouniversitario, identificacion, foto, notas, plan]
            
            save = save_profile_processes.update_documents(data_status, data_documents)
            
            if save:
                # Procesar los datos y generar la respuesta en JSON
                response_data = {'result': 'ok'}
                return JsonResponse(response_data)
            else:
                response_data = {'error': 'Invalid request method'}
                return JsonResponse(response_data, status=400)
            
        except KeyError:
            response_data = {'error': 'Invalid request method'}
            return JsonResponse(response_data, status=400)
    else:
        # Si la petición no es POST, devuelve un error
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=400)
    
@csrf_exempt
def user_update(request):
    #http://192.168.8.136:8000/user-update/
    
    # {
    #     "data": {
    #         "id": 117580049,
    #         "correo": "jelopmen@hotmail.com"
    #     }
    # }
    
    user = request.user
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            response_data = {'error': 'Invalid JSON'}
            return JsonResponse(response_data, status=400)
            
        try:
            id_value = data['data']['id']
            email_value = data['data']['correo']
            
            data = [id_value, email_value]
            
            save = save_profile_processes.update_user_prospecto(data)
            
            if save:
                # Procesar los datos y generar la respuesta en JSON
                save_profile_processes.update_user_status(request, 'matricula', True)
                response_data = {'result': 'ok'}
                return JsonResponse(response_data)
            else:
                response_data = {'error': 'Invalid request method'}
                return JsonResponse(response_data, status=400)
            
        except KeyError:
            response_data = {'error': 'Invalid request method'}
            return JsonResponse(response_data, status=400)
    else:
        # Si la petición no es POST, devuelve un error
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=400)
    
@csrf_exempt
def solicitud_form(request):
    #http://192.168.8.136:8000/solicitud-form/
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            response_data = {'error': 'Invalid JSON'}
            return JsonResponse(response_data, status=400)
            
        try:
            if data is not None:
                print (data)
                # Procesar los datos y generar la respuesta en JSON
                response_data = {'result': 'ok'}
                return JsonResponse(response_data)
            else:
                response_data = {'error': 'Invalid request method'}
                return JsonResponse(response_data, status=400)
            
        except KeyError:
            response_data = {'error': 'Invalid request method'}
            return JsonResponse(response_data, status=400)
    else:
        # Si la petición no es POST, devuelve un error
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=400)