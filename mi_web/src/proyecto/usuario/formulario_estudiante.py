from django import forms
from .models import estudiantes

class FormularioEstudiantes(forms.ModelForm):
    class Meta:
        model = estudiantes
        fields = ('Cedula', 'nombre', 'primer_apellido',
                  'segundo_apellido', 'fecha_nacimiento', 'phone_tutor', 
                  'correo_estudiante', 'password', 'pago_realizado','documentos_presentados')