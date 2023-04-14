$(document).ready(function () {
    Verificacion();
});

function Verificacion() {
    $(".progress").each(function () {
        var value = $(this).attr('data-value');
        var left = $(this).find('.progress-left .progress-bar');
        var right = $(this).find('.progress-right .progress-bar');

        if (value > 0) {
            if (value <= 50) {
                right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
            } else {
                right.css('transform', 'rotate(180deg)')
                left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
            }
        }
    })

    function percentageToDegrees(percentage) {
        return percentage / 100 * 360
    }
}

document.addEventListener('DOMContentLoaded', () => {
    var valor;
    var estado = document.getElementById('estado');
    var convalidacion = document.getElementById('conv').value;

    var doc_titulo = document.getElementById('tituloTF').value;
    var doc_ident = document.getElementById('identificacionTF').value;
    var doc_pasaporte = document.getElementById('fotoTF').value;
    var doc_notas = document.getElementById('notaTF').value;
    var doc_estudio = document.getElementById('planTF').value;

    if (estado !== null) {
        valor = estado.textContent;
    } else {
        console.log('El elemento span no existe en el documento');
    }

    var progressBar = document.getElementById("barra_progreso");
    var comentarios = document.getElementById("comentarios");
    var estadotext = document.getElementById("comentarios");

    var titulo1 = document.getElementById("titulo1");
    var titulo2 = document.getElementById("titulo2");

    var identificacion1 = document.getElementById("identificacion1");
    var identificacion2 = document.getElementById("identificacion2");

    var pasaporte1 = document.getElementById("pasaporte1");
    var pasaporte2 = document.getElementById("pasaporte2");

    var notas1 = document.getElementById("notas1");
    var notas2 = document.getElementById("notas2");

    var estudio1 = document.getElementById("estudio1");
    var estudio2 = document.getElementById("estudio2");

    var divtitulo = document.getElementById("div_titulo");
    var dividentificacion = document.getElementById("div_identificacion");
    var divpasaporte = document.getElementById("div_pasaporte");
    var divnotas = document.getElementById("div_notas");
    var divestudio = document.getElementById("div_estudio");

    var divconvalidacion = document.getElementById("div_convalidacion");

    var divprogretitulo = document.getElementById("div_progre_titulo");
    var divprogreident = document.getElementById("div_progre_ident");
    var divprogrepasaporte = document.getElementById("div_progre_pasaporte");
    var divprogrenotas = document.getElementById("div_progre_notas");
    var divprogreestudio = document.getElementById("div_progre_estudio");

    var imgtitulo = document.getElementById("img_titulo");
    var imgidentificacion = document.getElementById("img_ident");
    var imgpasaporte = document.getElementById("img_pasaporte");
    var imgnotas = document.getElementById("img_notas");
    var imgestudio = document.getElementById("img_estudio");

    // Obtener el estado del objeto de la base de datos en Django
    var documentocargado = document.getElementById("documentocargado");
    switch (valor) {
        case "Enviado":
            progressBar.style.width = "10%";
            break;
        case "Recibido":
            progressBar.style.width = "25%";
            break;
        case "En Revisión":
            progressBar.style.width = "50%";
            break;
        case "Revisión de Convalidaciones":
            progressBar.style.width = "75%";
            break;
        case "Aprobado":
            progressBar.style.width = "100%";
            progressBar.style.backgroundColor = "green";
            aprobado();
            break;
        case "Corrección Requerida":
            progressBar.style.width = "75%";
            progressBar.style.backgroundColor = "rgb(255, 80, 0)";
            var btnT = document.getElementById('btnT');
            var btnI = document.getElementById('btnI');
            var btnF = document.getElementById('btnF');
            var btnN = document.getElementById('btnN');
            var btnP = document.getElementById('btnP');
            btnT.onclick = function () {
                cambiarestado('titulo');
            };
            btnI.onclick = function () {
                cambiarestado('identificacion');
            };
            btnF.onclick = function () {
                cambiarestado('foto');
            };
            btnN.onclick = function () {
                cambiarestado('nota');
            };
            btnP.onclick = function () {
                cambiarestado('plan');
            };
            correccion();
            break;
        case "Rechazado":
            progressBar.style.width = "50%";
            break;
        default:
            progressBar.style.width = "0%";
    }

    if (convalidacion == "True") {
        divconvalidacion.style.display = "flex";
    }

    function correccion() {
        if (doc_titulo == "False") {
            divtitulo.style.display = "block";
            titulo1.classList.remove('border-primary');
            titulo1.classList.add('border-danger');

            titulo2.classList.remove('border-primary');
            titulo2.classList.add('border-danger');

            imgtitulo.src = "../../../../static/img/error.png";
            imgtitulo.width = 80;
            imgtitulo.height = 80;

            divprogretitulo.setAttribute("data-value", "0");
        }

        if (doc_ident == "False") {
            dividentificacion.style.display = "block";
            identificacion1.classList.remove('border-primary');
            identificacion1.classList.add('border-danger');

            identificacion2.classList.remove('border-primary');
            identificacion2.classList.add('border-danger');

            imgidentificacion.src = "../../../../static/img/error.png";
            imgidentificacion.width = 80;
            imgidentificacion.height = 80;

            divprogreident.setAttribute("data-value", "0");
        }

        if (doc_pasaporte == "False") {
            divpasaporte.style.display = "block";
            pasaporte1.classList.remove('border-primary');
            pasaporte1.classList.add('border-danger');

            pasaporte2.classList.remove('border-primary');
            pasaporte2.classList.add('border-danger');

            imgpasaporte.src = "../../../../static/img/error.png";
            imgpasaporte.width = 80;
            imgpasaporte.height = 80;

            divprogrepasaporte.setAttribute("data-value", "0");
        }

        if (convalidacion == "True") {
            if (doc_notas == "False") {
                divnotas.style.display = "block";
                notas1.classList.remove('border-primary');
                notas1.classList.add('border-danger');

                notas2.classList.remove('border-primary');
                notas2.classList.add('border-danger');

                imgnotas.src = "../../../../static/img/error.png";
                imgnotas.width = 80;
                imgnotas.height = 80;

                divprogrenotas.setAttribute("data-value", "0");
            }

            if (doc_estudio == "False") {
                divestudio.style.display = "block";
                estudio1.classList.remove('border-primary');
                estudio1.classList.add('border-danger');

                estudio2.classList.remove('border-primary');
                estudio2.classList.add('border-danger');

                imgestudio.src = "../../../../static/img/error.png";
                imgestudio.width = 80;
                imgestudio.height = 80;

                divprogreestudio.setAttribute("data-value", "0");
            }
        }

    }

    function aprobado() {
        titulo1.classList.remove('border-primary');
        titulo1.classList.add('border-success');

        titulo2.classList.remove('border-primary');
        titulo2.classList.add('border-success');

        imgtitulo.src = "../../../../static/img/check.png";
        imgtitulo.width = 170;
        imgtitulo.height = 170;

        divprogretitulo.setAttribute("data-value", "100");

        identificacion1.classList.remove('border-primary');
        identificacion1.classList.add('border-success');

        identificacion2.classList.remove('border-primary');
        identificacion2.classList.add('border-success');

        imgidentificacion.src = "../../../../static/img/check.png";
        imgidentificacion.width = 170;
        imgidentificacion.height = 170;

        divprogreident.setAttribute("data-value", "100");

        pasaporte1.classList.remove('border-primary');
        pasaporte1.classList.add('border-success');

        pasaporte2.classList.remove('border-primary');
        pasaporte2.classList.add('border-success');

        imgpasaporte.src = "../../../../static/img/check.png";
        imgpasaporte.width = 170;
        imgpasaporte.height = 170;

        divprogrepasaporte.setAttribute("data-value", "100");

        notas1.classList.remove('border-primary');
        notas1.classList.add('border-success');

        notas2.classList.remove('border-primary');
        notas2.classList.add('border-success');

        imgnotas.src = "../../../../static/img/check.png";
        imgnotas.width = 170;
        imgnotas.height = 170;

        divprogrenotas.setAttribute("data-value", "100");

        estudio1.classList.remove('border-primary');
        estudio1.classList.add('border-success');

        estudio2.classList.remove('border-primary');
        estudio2.classList.add('border-success');

        imgestudio.src = "../../../../static/img/check.png";
        imgestudio.width = 170;
        imgestudio.height = 170;

        divprogreestudio.setAttribute("data-value", "100");
    }



    function cambiarestado(documento) {
        console.log("boton");
        if (documento == "titulo") {
            divtitulo.style.display = "none";
            titulo1.classList.remove('border-danger');
            titulo1.classList.add('border-primary');

            titulo2.classList.remove('border-danger');
            titulo2.classList.add('border-primary');

            imgtitulo.src = "../../../../static/img/pendiente.png";
            imgtitulo.width = 100;
            imgtitulo.height = 100;

            divprogretitulo.setAttribute("data-value", "50");
            documentocargado.value = "titulo";
            console.log(documentocargado);
            Verificacion();
        }

        if (documento == "identificacion") {
            dividentificacion.style.display = "none";
            identificacion1.classList.remove('border-danger');
            identificacion1.classList.add('border-primary');

            identificacion2.classList.remove('border-danger');
            identificacion2.classList.add('border-primary');

            imgidentificacion.src = "../../../../static/img/pendiente.png";
            imgidentificacion.width = 170;
            imgidentificacion.height = 170;

            divprogreident.setAttribute("data-value", "50");
            documentocargado.value = "identificacion";
            console.log(documentocargado);
            Verificacion();
        }

        if (documento == "foto") {
            divpasaporte.style.display = "none";
            pasaporte1.classList.remove('border-danger');
            pasaporte1.classList.add('border-primary');

            pasaporte2.classList.remove('border-danger');
            pasaporte2.classList.add('border-primary');

            imgpasaporte.src = "../../../../static/img/pendiente.png";
            imgpasaporte.width = 170;
            imgpasaporte.height = 170;


            divprogrepasaporte.setAttribute("data-value", "50");
            documentocargado.value = "foto";
            console.log(documentocargado);
            Verificacion();
        }

        if (documento == "notas") {
            divnotas.style.display = "none";
            notas1.classList.remove('border-danger');
            notas1.classList.add('border-primary');

            notas2.classList.remove('border-danger');
            notas2.classList.add('border-primary');

            imgnotas.src = "../../../../static/img/pendiente.png";
            imgnotas.width = 170;
            imgnotas.height = 170;


            divprogrenotas.setAttribute("data-value", "50");
            documentocargado.value = "notas";
            console.log(documentocargado);
            Verificacion();
        }

        if (documento == "notas") {
            divnotas.style.display = "none";
            notas1.classList.remove('border-danger');
            notas1.classList.add('border-primary');

            notas2.classList.remove('border-danger');
            notas2.classList.add('border-primary');

            imgnotas.src = "../../../../static/img/pendiente.png";
            imgnotas.width = 170;
            imgnotas.height = 170;


            divprogrenotas.setAttribute("data-value", "50");
            documentocargado.value = "notas";
            console.log(documentocargado);
            Verificacion();
        }

        if (documento == "plan") {
            divestudio.style.display = "none";
            estudio1.classList.remove('border-danger');
            estudio1.classList.add('border-primary');

            estudio2.classList.remove('border-danger');
            estudio2.classList.add('border-primary');

            imgestudio.src = "../../../../static/img/pendiente.png";
            imgestudio.width = 170;
            imgestudio.height = 170;


            divprogreestudio.setAttribute("data-value", "50");
            documentocargado.value = "plan";
            console.log(documentocargado);
            Verificacion();
        }
    }
});