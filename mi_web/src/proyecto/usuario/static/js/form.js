$(document).ready(function () {
    Verificacion();
    $('[data-bs-toggle="popover"]').popover({
        placement : 'top',
        html : true,
        title : 'User Info <a href="#" class="close" data-bs-dismiss="alert">&times;</a>',
        content : '<a type="button" id="btnPoper" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Ver archivo</a>'
    });
    $(document).on("click", ".popover .close" , function(){
        $(this).parents(".popover").popover('hide');
    });
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

    var divconvalidacion = document.getElementById("div_convalidacion");
    var divconvalidacion2 = document.getElementById("div_convalidacion2");

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

            var btnINT = document.getElementById('btnINT');
            var btnINI = document.getElementById('btnINI');
            var btnINF = document.getElementById('btnINF');
            var btnINN = document.getElementById('btnINN');
            var btnINP = document.getElementById('btnINP');

            btnINT.onclick = function (){
                cambiarInput('titulo');
            }

            btnINI.onclick = function (){
                cambiarInput('identificacion');
            }

            btnINF.onclick = function (){
                cambiarInput('foto');
            }

            btnINN.onclick = function (){
                cambiarInput('nota');
            }

            btnINP.onclick = function (){
                cambiarInput('plan');
            }
            correccion();
            break;
        case "Rechazado":
            progressBar.style.width = "50%";
            break;
        default:
            progressBar.style.width = "0%";
    }

    if (convalidacion == "True") {
        divconvalidacion.style.display = "block";
        divconvalidacion2.style.display = "block";
    }

    function correccion() {
        var spinner1 = document.getElementById("spinner1");
        var spinner2 = document.getElementById("spinner2");
        var spinner3 = document.getElementById("spinner3");
        var spinner4 = document.getElementById("spinner4");
        var spinner5 = document.getElementById("spinner5");
        var cardT = document.getElementById("cardT");
        var cardI = document.getElementById("cardI");
        var cardF = document.getElementById("cardF");
        var cardN = document.getElementById("cardN");
        var cardP = document.getElementById("cardP");
        if (doc_titulo == "False") {

            imgtitulo.src = "../../../../static/img/error.png";
            imgtitulo.hidden = false;
            cardT.style.backgroundColor = '#FF7F45';
            spinner1.style.display = "none";
            imgtitulo.width = 35;
            imgtitulo.height = 35;
        }

        if (doc_ident == "False") {

            imgidentificacion.src = "../../../../static/img/error.png";
            cardI.style.backgroundColor = '#FF7F45';
            imgidentificacion.hidden = false;
            spinner2.style.display = "none";
            imgidentificacion.width = 35;
            imgidentificacion.height = 35;

        }

        if (doc_pasaporte == "False") {

            imgpasaporte.src = "../../../../static/img/error.png";
            cardF.style.backgroundColor = '#FF7F45';
            imgpasaporte.hidden = false;
            spinner3.style.display = "none";
            imgpasaporte.width = 35;
            imgpasaporte.height = 35;

        }

        if (convalidacion == "True") {
            if (doc_notas == "False") {

                imgnotas.src = "../../../../static/img/error.png";
                cardN.style.backgroundColor = '#FF7F45';
                imgnotas.hidden = false;
                spinner4.style.display = "none";
                imgnotas.width = 35;
                imgnotas.height = 35;

            }

            if (doc_estudio == "False") {

                imgestudio.src = "../../../../static/img/error.png";
                cardP.style.backgroundColor = '#FF7F45';
                imgestudio.hidden = false;
                spinner5.style.display = "none";
                imgestudio.width = 35;
                imgestudio.height = 35;


            }
        }

    }

    function aprobado() {

        var spinner1 = document.getElementById("spinner1");
        var spinner2 = document.getElementById("spinner2");
        var spinner3 = document.getElementById("spinner3");
        var spinner4 = document.getElementById("spinner4");
        var spinner5 = document.getElementById("spinner5");
        var cardT = document.getElementById("cardT");
        var cardI = document.getElementById("cardI");
        var cardF = document.getElementById("cardF");
        var cardN = document.getElementById("cardN");
        var cardP = document.getElementById("cardP");

        imgtitulo.src = "../../../../static/img/check.png";
        imgtitulo.hidden = false;
        cardT.style.backgroundColor = '#7FFF7F';
        spinner1.style.display = "none";
        imgtitulo.width = 50;
        imgtitulo.height = 50;


        imgidentificacion.src = "../../../../static/img/check.png";
        imgidentificacion.hidden = false;
        cardI.style.backgroundColor = '#7FFF7F';
        spinner2.style.display = "none";
        imgidentificacion.width = 50;
        imgidentificacion.height = 50;


        imgpasaporte.src = "../../../../static/img/check.png";
        imgpasaporte.hidden = false;
        cardF.style.backgroundColor = '#7FFF7F';
        spinner3.style.display = "none";
        imgpasaporte.width = 50;
        imgpasaporte.height = 50;


        imgnotas.src = "../../../../static/img/check.png";
        imgnotas.hidden = false;
        cardN.style.backgroundColor = '#7FFF7F';
        spinner4.style.display = "none";
        imgnotas.width = 50;
        imgnotas.height = 50;


        imgestudio.src = "../../../../static/img/check.png";
        imgestudio.hidden = false;
        spinner5.style.display = "none";
        cardP.style.backgroundColor = '#7FFF7F';
        imgestudio.width = 50;
        imgestudio.height = 50;

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

    function cambiarInput(archivo){
        var formularioT = document.getElementById("div_titulo");
        var formularioI = document.getElementById("div_identificacion");
        var formularioF = document.getElementById("div_pasaporte");
        var formularioN = document.getElementById("div_notas");
        var formularioP = document.getElementById("div_estudio");
        formularioT.style.display = "none";
        formularioI.style.display = "none";
        formularioF.style.display = "none";
        formularioN.style.display = "none";
        formularioP.style.display = "none";
        if (archivo === 'titulo'){
            formularioT.style.display = "block";
        }
        else if (archivo === 'identificacion'){
            formularioI.style.display = "block";
        }
    
        else if (archivo === 'foto'){
            formularioF.style.display = "block";
        }
    
        else if (archivo === 'nota'){
            formularioN.style.display = "block";
        }
    
        else if (archivo === 'plan'){
            formularioP.style.display = "block";
        }
    }
});