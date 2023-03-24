function change(){
    var selectValue = document.getElementById('tipo');
    var input = document.getElementById('identificacion');
    if (selectValue.value === 'Cédula'){
        input.oninput = function() {

            this.value = this.value.replace(/[^0-9]/g, '');
        }
        input.value = '';
        input.removeAttribute('disabled');
        input.setAttribute('minLength', '9');
        input.setAttribute('maxLength', '9');
    }else if (selectValue.value === 'Dimex'){

        input.oninput = function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        }
        input.value = '';
        input.removeAttribute('disabled');
        input.setAttribute('minLength', '11');
        input.setAttribute('maxLength', '12');
    } else if (selectValue.value === 'Pasaporte'){

        input.oninput = null;
        input.value = '';
        input.removeAttribute('disabled');
        input.setAttribute('minLength', '9');
        input.setAttribute('maxLength', '20');
    }

    else if (selectValue.value === 'Refugiado'){

        input.oninput = function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        }
        input.value = '';
        input.removeAttribute('disabled');
        input.setAttribute('minLength', '12');
        input.setAttribute('maxLength', '12');
    }

    else if (selectValue.value === 'Permiso'){

        input.oninput = null;
        input.value = '';
        input.removeAttribute('disabled');
        
    }

    else if (selectValue.value === 'Cédula Residente'){

        input.oninput = function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        }
        input.value = '';
        input.removeAttribute('disabled');
        input.setAttribute('minLength', '12');
        input.setAttribute('maxLength', '12');
    }
}

document.addEventListener("keyup", function(event) {
    if(event.key === 'Backspace'){
            var nombre = document.getElementById('nombre');
            var primer = document.getElementById('primerapellido');
            var segundo = document.getElementById('segundoapellido');
            nombre.value = '';
            nombre.removeAttribute('readonly');
            primer.value = '';
            primer.removeAttribute('readonly');
            segundo.value = '';
            segundo.removeAttribute('readonly');
    }
});


