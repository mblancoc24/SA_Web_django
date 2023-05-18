from django.templatetags.static import static
def custom_context(request):
    # Define las variables de contexto que deseas utilizar
    logo_url = 'https://uia.ac.cr/home/dist/img/Logo-black.png'
    copyRigth= '© 2023. Universidad<br> Internacional de las<br> Américas'
    footerCorreo = 'info@uia.ac.cr'
    footerContacto1 = 'San José: 2212-5500'
    footerContacto2 = 'Heredia: 2238-4131'
    formPrimerIngreso = static('img/primer_ingreso.png')
    formPosgrados = static('img/posgrados.png')
    formCursoLibre = static('img/cursos_libres.png')
    
    # Retorna un diccionario de variables de contexto
    return {
        'logo_url': logo_url,
        'copyRigth': copyRigth,
        'footerCorreo': footerCorreo,
        'footerContacto1': footerContacto1,
        'footerContacto2': footerContacto2,
        'formPrimerIngreso': formPrimerIngreso,
        'formPosgrados': formPosgrados,
        'formCursoLibre': formCursoLibre,
    }