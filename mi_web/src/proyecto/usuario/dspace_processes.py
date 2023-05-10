import requests
import json
from django.contrib.auth.models import User
from datetime import date
from .api_queries import update_urls

class dspace_processes():
    
    def dspace_first_admission(request, files):
        session = requests.Session()
        user = request.user
        user = User.objects.get(username=user.username)
        user_data = request.session.get('user_info')
        
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
                "dc.title": [{"value": user_data['identificacion']}],
                "dc.contributor.author": [{"value": user_data['nombre'] +" "+ user_data['primer_apellido'] +" "+ user_data['segundo_apellido']}],
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
                urls_dspace.append('http://dspace.uia.ac.cr:8080/server/api/core/bitstreams/'+bitstreams_id+'/content')
                if 'tituloeducacion' in record['nombre']:
                    urls_dspace.append('N/A')
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
         
    def dspace_file_correction(request, file, file_name):
        session = requests.Session()
        user = request.user
        user = User.objects.get(username=user.username)
        
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

        # Obtencion de ITEM en coleccion determinada
        headers = {
            "Authorization": token,
            "X-XSRF-TOKEN": csrf_token_login
        }
        upload_url = "http://dspace.uia.ac.cr:8080/server/api/core/items"
        response = session.get(upload_url, headers=headers)
        items = json.loads(response.text)
        item_id = ""
        for item in items['_embedded']['items']:
            if item['name'] == user.username:
                item_id = item['uuid']
                break
            
        # Obtencion de BUNDLE en coleccion determinada
        bundle_url = "http://dspace.uia.ac.cr:8080/server/api/core/items/"+item_id+"/bundles"
        response = session.get(bundle_url, headers=headers)
        bundles = json.loads(response.text)
        bundle_id = ""
        for bundle in bundles['_embedded']['bundles']:
            if bundle['name'] == 'PRIMER_INGRESO':
                bundle_id = bundle['uuid']
                break
            
        # Obtencion de BITSTREAM en bundle determinada
        bitstream_url = "http://dspace.uia.ac.cr:8080/server/api/core/bundles/"+bundle_id+"/bitstreams"
        response = session.get(bitstream_url, headers=headers)
        bitstreams = json.loads(response.text)
        bitstream_id = ""
        for bitstream in bitstreams['_embedded']['bitstreams']:
            if file_name in bitstream['name']:
                bitstream_id = bitstream['uuid']
                break
            
        # Eliminacion de BITSTREAM en bundle determinada
        bitstream_url = "http://dspace.uia.ac.cr:8080/server/api/core/bitstreams/"+bitstream_id
        response = session.delete(bitstream_url, headers=headers)
        if response.status_code == 204:
            print('Se elimino exitosamente')
        else:
            print('Error al eliminar')
        
        # Ingresar nuevo BITSTREAM en bundle determinada
        for dt in file:
            record = file[dt]
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
            url = 'http://dspace.uia.ac.cr:8080/server/api/core/bitstreams/'+bitstreams_id+'/content'
            
            update_urls(request, url, file_name)
        else:
            print('Error al enviar el archivo')
                
        # Cierre de sesión
        logout_url = 'http://dspace.uia.ac.cr:8080/server/api/authn/logout'

        response = session.post(logout_url, headers=headers)

        if response.status_code == 204:
            print('Sesión cerrada exitosamente')
            return True
        else:
            print('Error al cerrar la sesión')
         
    def dspace_docs_visualization(data_url):
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
            
        headers = {
            "Authorization": token,
            "X-XSRF-TOKEN": csrf_token_login
        }
        data_content = []
        if 'id_estudiante' in data_url:
            del data_url['id_estudiante']
        for url in data_url.values():
            if url != 'N/A':
                upload_url = url
                response = session.get(upload_url, headers=headers)
                if response.status_code == 200:
                    print('Archivo enviado con éxito')
                    data_content.append(response)
                else:
                    print('Error al enviar el archivo')
        return data_content
   
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
    
    def name_file_correction_standardization(request, file, type):
        user = request.user
        
        file_type = file.name
        file_termination = file_type.split(".")
        
        if type == 'tituloeducacion':
            new_file = 'tituloeducacion_'+ user.username +'.'+ file_termination[1]
        elif type == 'identificacion':
            new_file = 'identificacion_'+ user.username +'.'+ file_termination[1]
        elif type == 'fotoperfil':
            new_file = 'fotoperfil_'+ user.username +'.'+ file_termination[1]
        elif type == 'record_academico':
            new_file = 'record_academico_'+ user.username +'.'+ file_termination[1]
        elif type == 'plan_estudio':
            new_file = 'plan_estudio_'+ user.username +'.'+ file_termination[1]
        
        file_updated = {
            'file': {
                'nombre': new_file,
                'archivo': file,
                'descripcion': 'Título de Educación Media',
                'tipo': file.content_type
            }
        }
    
        return file_updated