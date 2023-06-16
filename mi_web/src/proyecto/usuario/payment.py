import hashlib
from django.http import JsonResponse
from .models import fotoperfil
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.files.base import ContentFile
from PIL import Image
from .save_processes import save_profile_processes

class PaymentApproved(LoginRequiredMixin, View):
    context_object_name = 'payment'
    template_name = 'Dashboard/Prospecto/pago_realizado.html'

    def get_context_data(self, **kwargs):
        user = self.request.user

        response = self.request.GET.get('response')
        responsetext = self.request.GET.get('responsetext')
        authcode = self.request.GET.get('authcode')
        transactionid = self.request.GET.get('transactionid')
        avsresponse = self.request.GET.get('avsresponse')
        cvvresponse = self.request.GET.get('cvvresponse')
        orderid = self.request.GET.get('orderid')
        response_code = self.request.GET.get('response_code')
        time = self.request.GET.get('time')
        amount = self.request.GET.get('amount')
        hash = self.request.GET.get('hash')

        hash_respuesta = calcular_hash_respuesta(self.request, orderid, amount, response, transactionid, avsresponse, cvvresponse, time)

        verification = verificar_hash_respuesta(self.request, hash, hash_respuesta)

        if verification and response_code == '100':
            pago = 100
        elif response_code == '200' or response_code == '202':
            pago = 200
        elif response_code == '300':
           pago = 300
        else:
            pago = 300

        try:
            fotoperfil_obj = fotoperfil.objects.get(user=user.pk)
            imagen_url = Image.open(ContentFile(fotoperfil_obj.archivo))
            context = {
                'user': user,
                'fotoperfil': imagen_url,
                'status': self.kwargs['status'],
                'pago': pago,
                'id': self.kwargs['id'],
                'type': self.kwargs['type'],
            }
        except fotoperfil.DoesNotExist:
            context = {
                'user': user,
                'status': self.kwargs['status'],
                'pago': pago,
                'id': self.kwargs['id'],
                'type': self.kwargs['type'],
            }
        return context
        
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

@login_required
def obtener_hash_entrada(request):
    orderid = request.session.get('orderid')
    amount = "5.00"
    time = request.session.get('timePy')
    key = obtener_key(request)

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

    request.session['hash_entrada'] = hash_md5

    return JsonResponse(hash_md5, safe=False)

@login_required
def calcular_hash_respuesta(request, orderid, amount, response, transactionid, avsresponse, cvvresponse, time):

    key = obtener_key(request)

    # Concatenamos los valores en un formato específico
    data = "|".join([orderid, amount, response, transactionid, avsresponse, cvvresponse, time, key])

    # Calcular el hash MD5
    md5_hash = hashlib.md5(data.encode()).hexdigest()   

    return md5_hash

@login_required
def verificar_hash_respuesta(request, hash_generado, hash_recibido):
    return hash_generado == hash_recibido

@login_required
def obtener_key(request):
    key = "fEDMWkhxH48M52D7AudqhB6anTU5F95g"
    return key

@login_required
def obtener_keyiD(request):
    keyID = "8049106"
    return JsonResponse(keyID, safe=False)

