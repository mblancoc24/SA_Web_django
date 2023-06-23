function enviarCorreo(event) {
    event.preventDefault();
    var data = {};
    var identificacion = document.getElementById('idE');
    var status = document.getElementById('StatusE');
    var type = document.getElementById('typeE');

    var nombre = document.getElementById('nombre');
    var correo = document.getElementById('correo');
    var correoSend = document.getElementById('correoSend');
    var categorias = document.getElementById('categorias');
    var mensaje = document.getElementById('mensaje');
    const radios = document.querySelectorAll('input[name="departamento"]');
    let valorSeleccionado;

    radios.forEach((radio) => {
        if (radio.checked) {
            valorSeleccionado = radio.value;
        }
    });

    let correoSendNew;
    if (correoSend.innerText === 'true') {
        if (valorSeleccionado === 'Registro') {
            correoSendNew = 'victorfern27@gmail.com';
        } else {
            correoSendNew = 'victorfern48@gmail.com';
        }
    } else {
        if (valorSeleccionado === 'Registro') {
            correoSendNew = 'victor2722v@gmail.com';
        } else {
            correoSendNew = 'victfern48@gmail.com';
        }
    }
    data.nombre = nombre.value;
    data.correo = correo.value;
    data.correoSend = correoSendNew;
    data.departamento = valorSeleccionado;
    data.categorias = categorias.value;
    data.mensaje = mensaje.value;
    var jsonString = JSON.stringify(data);
    var xhr = new XMLHttpRequest();
    var url = `/${type.textContent}/${identificacion.textContent}/${status.textContent}/envioConsulta/`;
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    var csrfToken = getCSRFToken();
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                console.log(response);

                if (response.response) {
                    closeModal();
                    showToast("success", valorSeleccionado);
                } else {
                    closeModal();
                    showToast("error", valorSeleccionado);
                }
            }

        };
    }
    xhr.send(jsonString);
}

function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, 'csrftoken'.length + 1) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function closeModal() {
    $('#modal_contactenos').modal('hide');
}

function showToast(type, departamento) {
    var toastElement = document.getElementById('liveToast');
    var toastBody = toastElement.querySelector('.toast-body');
    var toastTittle = toastElement.querySelector('#titleToast');
    var toastCloseButton = toastElement.querySelector('.btn-close');
    var toastHeaderImg = toastElement.querySelector('#img_check');

    if (type === 'error') {
        toastTittle.innerText = 'Error en el envió de correo al departamento ' + departamento;
        toastElement.classList.add('bg-danger');
        toastHeaderImg.src = "../../../../static/img/error.png";
    } else {
        toastTittle.innerText = 'Se envio correctamente el correo al departamento ' + departamento;
        toastElement.classList.remove('bg-danger');
        toastHeaderImg.src = "../../../../static/img/check.png";
    }
    toastCloseButton.addEventListener('click', function () {
        var bootstrapToast = bootstrap.Toast.getInstance(toastElement);
        bootstrapToast.hide();
    });
    var bootstrapToast = new bootstrap.Toast(toastElement, { delay: 8000 });
    bootstrapToast.show();
}