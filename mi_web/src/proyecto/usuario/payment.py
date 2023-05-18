import hashlib
import random
from django.http import JsonResponse
import requests

def calcular_hash_entrada(request, orderid, amount, time):
    # orderid = "test"
    # amount = "1.00"
    # time = "1279302634"
    # key = "23232332222222222222222222222222"

    if 'key' in request.session:
        key = request.session.get('key')
    else:
        create = generar_codigo_aleatorio()
        if create:
            key = request.session.get('key')


    # Concatenamos los valores en un formato específico
    cadena = f"{orderid}|{amount}|{time}|{key}"

    # Creamos un objeto hash MD5
    md5 = hashlib.md5()

    # Convertimos la cadena a una secuencia de bytes codificada en UTF-8
    cadena_bytes = cadena.encode('utf-8')

    # Actualizamos el hash con la cadena
    md5.update(cadena_bytes)

    # Obtenemos el hash MD5 en formato hexadecimal
    hash_md5 = md5.hexdigest()

    return JsonResponse(hash_md5, safe=False)

def calcular_hash_respuesta(request, orderid, amount, response, transactionid, avsresponse, cvvresponse, time):
    # orderid = "test"
    # amount = "1.00"
    # response = "1"
    # transactionid = "273247169"
    # avsresponse = "N"
    # cvvresponse = "N"
    # time = "1279302634"
    # key = "23232332222222222222222222222222"

    if 'key' in request.session:
        key = request.session.get('key')
    else:
        return False

    # Concatenamos los valores en un formato específico
    cadena = f"{orderid}|{amount}|{response}|{transactionid}|{avsresponse}|{cvvresponse}|{time}|{key}"

    # Creamos un objeto hash MD5
    md5 = hashlib.md5()

    # Convertimos la cadena a una secuencia de bytes codificada en UTF-8
    cadena_bytes = cadena.encode('utf-8')

    # Actualizamos el hash con la cadena
    md5.update(cadena_bytes)

    # Obtenemos el hash MD5 en formato hexadecimal
    hash_md5 = md5.hexdigest()

    return JsonResponse(hash_md5, safe=False)

def verificar_hash_respuesta(hash_generado, hash_recibido):
    return hash_generado == hash_recibido

def generar_codigo_aleatorio(request):
    codigo = ""
    for _ in range(32):
        digito = random.randint(0, 9)
        codigo += str(digito)

    request.session['key'] = codigo
    return True
