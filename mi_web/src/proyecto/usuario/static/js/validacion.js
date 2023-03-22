function change(){
    var selectValue = document.getElementById('tipo');
    var input = document.getElementById('identificacion');
    if (selectValue.value === 'Cédula'){
        input.oninput = function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        }
        input.minLength = 9;
        input.maxLength = 9;
    }else if (selectValue.value === 'Dimex'){
        input.oninput = function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        }
        input.minLength = 12;
        input.maxLength = 12;
    }else if (selectValue.value === 'Pasaporte'){
        input.minLength = 7;
        input.maxLength = 7;
    }

    else if (selectValue.value === 'Cédula Jurídica'){
        input.oninput = function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        }
        input.minLength = 11;
        input.maxLength = 11;
    }
}

