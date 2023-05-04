import requests
import json
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from .backends import MicrosoftGraphBackend
from datetime import date


class dspace_processes():
    
    def dspace_first_admission(request, files):
        session = requests.Session()
        user = request.user
        user = User.objects.get(username=user.username)
        user_type = MicrosoftGraphBackend.user_type(request)
        user_data = MicrosoftGraphBackend.get_user_data(request, user_type)
        
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

        # Creacion de ITEM en coleccion determinada
        headers = {
            'Content-Type': 'application/json',
            "Authorization": token,
            "X-XSRF-TOKEN": csrf_token_login
        }
        upload_url = "http://dspace.uia.ac.cr:8080/server/api/core/items?owningCollection="+collection_id
        fecha_actual = date.today()
        metadata = {
            "name": "User",
            "metadata": {
                "dc.title": [{"value": user_data.identificacion}],
                "dc.contributor.author": [{"value": user_data.nombre +" "+ user_data.primer_apellido +" "+ user_data.segundo_apellido}],
                "dc.date.issued": [{"value": fecha_actual.strftime('%Y-%m-%d')}],
                "dc.publisher": [{"value": "Django"}]
            },
            "inArchive": True,
            "discoverable": True,
            "withdrawn": False,
            "type": "item"
        }
        response = session.post(upload_url, data=json.dumps(metadata), headers=headers)
        if response.status_code == 201:
            print('Archivo enviado con éxito')
            response_json = response.json()
            item_id = response_json['id']
        else:
            print('Error al enviar el archivo')
        
        #Creacion de BUNDLE dentro de ITEM creado anteriormente
        bundle = {
            "name": "PRIMER_INGRESO",
            "metadata": {
            }
        }
        headers = {  
            'Content-Type': 'application/json',
            "Authorization": token,
            "X-XSRF-TOKEN": csrf_token_login
        }
        upload_url = "http://dspace.uia.ac.cr:8080/server/api/core/items/"+item_id+"/bundles"
        response = session.post(upload_url, headers=headers, data=json.dumps(bundle))
        if response.status_code == 201:
            print('Archivo enviado con éxito')
            response_json = response.json()
            bundle_id = response_json['uuid']
        else:
            print('Error al enviar el archivo')
            
        #Creacion de BITSTREAMS dentro de BUNDLE creado anteriormente
        
        headers = {  
            "Authorization": token,           
            "X-XSRF-TOKEN": csrf_token_login,
        }
        
        urls_dspace = []
        
        for dt in files:
            record = files[dt]
            file_processed = record['archivo']
            data = {
                f'properties': '{ "name": "'+record['nombre']+'", "metadata": { "dc.description": [ { "value": "'+record['descripcion']+'", "language": null, "authority": null, "confidence": -1, "place": 0 }]}, "bundleName": "PRIMER_INGRESO" }'
            }
            
            data_file = {'file':(record['nombre'], file_processed, record['tipo'])}
    
            upload_url = "http://dspace.uia.ac.cr:8080/server/api/core/bundles/"+bundle_id+"/bitstreams"
            response = session.post(upload_url, headers=headers, data=data, files=data_file)
            if response.status_code == 201:
                print('Archivo enviado con éxito')
                response_json = response.json()
                bitstreams_id = response_json['id']
                urls_dspace.append('http://dspace.uia.ac.cr:4000/bitstreams/'+bitstreams_id+'/download')
            else:
                print('Error al enviar el archivo')
        
        # Cierre de sesión
        logout_url = 'http://dspace.uia.ac.cr:8080/server/api/authn/logout'

        response = session.post(logout_url, headers=headers)

        if response.status_code == 204:
            print('Sesión cerrada exitosamente')
            if len(urls_dspace) == 3:
                urls_dspace.append('N/A')
                urls_dspace.append('N/A')
                return urls_dspace
            else:
                return urls_dspace
        else:
            print('Error al cerrar la sesión')
            
    def name_standardization(request, files):
        user = request.user
        
        if files['convalidacion'] == 1:
            foto = files["foto"]
            titulo = files["titulo"]
            identificacion = files["identificacion"]
            certificacion = files["certificacion"]
            plan = files["plan"]
            
            foto_type = foto.name
            titulo_type = titulo.name
            identificacion_type = identificacion.name
            certificacion_type = certificacion.name
            plan_type = plan.name
            
            foto_termination = foto_type.split(".")
            titulo_termination = titulo_type.split(".")
            identificacion_termination = identificacion_type.split(".")
            certificacion_termination = certificacion_type.split(".")
            plan_termination = plan_type.split(".")
            
            new_foto = 'fotoperfil_'+ user.username +'.'+ foto_termination[1]
            new_titulo = 'tituloeducacion_'+ user.username +'.'+ titulo_termination[1]
            new_identificacion = 'identificacion_'+ user.username +'.'+ identificacion_termination[1]
            new_certificacion = 'record_academico_'+ user.username +'.'+ certificacion_termination[1]
            new_plan = 'plan_estudio_'+ user.username +'.'+ plan_termination[1]
            
            files_updated = {
                'titulo': {
                    'nombre': new_titulo,
                    'archivo': titulo,
                    'descripcion': 'Título de Educación Media',
                    'tipo': titulo.content_type
                },
                'identificacion': {
                    'nombre': new_identificacion,
                    'archivo': identificacion,
                    'descripcion': 'Identificación',
                    'tipo': identificacion.content_type
                },
                'certificacion': {
                    'nombre': new_certificacion,
                    'archivo': certificacion,
                    'descripcion': 'Record Academico o certificado de Notas del Curso',
                    'tipo': certificacion.content_type
                },
                'plan': {
                    'nombre': new_plan,
                    'archivo': plan,
                    'descripcion': 'Plan de Estudio - Contenido del Curso',
                    'tipo': plan.content_type
                },
                'foto': {
                    'nombre': new_foto,
                    'archivo': foto,
                    'descripcion': 'Foto de perfil tipo pasaporte',
                    'tipo': foto.content_type
                }
            }
        else:
            foto = files["foto"]
            titulo = files["titulo"]
            identificacion = files["identificacion"]
            
            foto_type = foto.name
            titulo_type = titulo.name
            identificacion_type = identificacion.name
            
            foto_termination = foto_type.split(".")
            titulo_termination = titulo_type.split(".")
            identificacion_termination = identificacion_type.split(".")
            
            new_foto = 'fotoperfil_'+ user.username +'.'+ foto_termination[1]
            new_titulo = 'tituloeducacion_'+ user.username +'.'+ titulo_termination[1]
            new_identificacion = 'identificacion_'+ user.username +'.'+ identificacion_termination[1]
            
            files_updated = {
                'titulo': {
                    'nombre': new_titulo,
                    'archivo': titulo,
                    'descripcion': 'Título de Educación Media',
                    'tipo': titulo.content_type
                },
                'identificacion': {
                    'nombre': new_identificacion,
                    'archivo': identificacion,
                    'descripcion': 'Identificación',
                    'tipo': identificacion.content_type
                },
                'foto': {
                    'nombre': new_foto,
                    'archivo': foto,
                    'descripcion': 'Foto de perfil tipo pasaporte',
                    'tipo': foto.content_type
                }
            }
        
        return files_updated