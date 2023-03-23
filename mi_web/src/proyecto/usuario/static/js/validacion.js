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
        input.setAttribute('minLength', '10');
        input.setAttribute('maxLength', '12');
    } else if (selectValue.value === 'Pasaporte'){

        input.oninput = null;
        input.value = '';
        input.removeAttribute('disabled');
        input.setAttribute('minLength', '9');
        input.setAttribute('maxLength', '20');
    }

    else if (selectValue.value === 'Cédula Jurídica'){

        input.oninput = function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        }
        input.value = '';
        input.removeAttribute('disabled');
        input.setAttribute('minLength', '11');
        input.setAttribute('maxLength', '11');
    }
}



