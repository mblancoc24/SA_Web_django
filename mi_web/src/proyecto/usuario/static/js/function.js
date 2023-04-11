function datacedula() {
    var input = document.getElementById("identificacion");
    var input2 = document.getElementById("tipo").value;

    var nacimiento = document.getElementById("dis_nacimiento");
    var genero = document.getElementById("dis_genero");
    var telefono = document.getElementById("dis_telefono");
    var nacionalidad = document.getElementById("dis_pais");
    var provincia = document.getElementById("dis_provincia");
    var canton = document.getElementById("dis_canton");
    var distrito = document.getElementById("dis_distrito");
    var cuenta_profesor = document.getElementById("cuenta_profesor");
    var cuenta_estudiante = document.getElementById("cuenta_estudiante");
    var cuenta_estudianteprofesor = document.getElementById("cuenta_estudianteprofesor");
    var es_profesor = document.getElementById("es_profesor");

    if (input.value.length >= 10 && input.value.length <= 12 && input2 === "Dimex" || "Cédula Residente" || "Refugiado") {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var datos = this.responseText;
                const datos_usuario = datos.split(",");

                if (datos_usuario[0].replace(/[\\\[\]"]/g, "") == "Existe") {
                    var nombre = document.getElementById("nombre");
                    var primer_apellido = document.getElementById("primerapellido");
                    var segundo_apellido = document.getElementById("segundoapellido");

                    nombre.readOnly = false;
                    primer_apellido.readOnly = false;
                    segundo_apellido.readOnly = false;
                }
            }
        };
        xhttp.open("GET", "/obtener-datos/?identificacion=" + encodeURIComponent(input.value), true);
        xhttp.send();

    }
    if (input.value.length === 9 && input2 === "Cédula") {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var datos = this.responseText;
                const datos_usuario = datos.split(",");

                var nombre = document.getElementById("nombre");
                var primer_apellido = document.getElementById("primerapellido");
                var segundo_apellido = document.getElementById("segundoapellido");

                nombre.value = datos_usuario[0].replace(/[\\\[\]"]/g, "").replace(/u00f1/g, 'ñ').replace(/u00D1/g, 'Ñ');
                primer_apellido.value = datos_usuario[1].replace(/[\\\[\]" ]/g, "").replace(/u00f1/g, 'ñ').replace(/u00D1/g, 'Ñ');
                segundo_apellido.value = datos_usuario[2].replace(/[\\\[\]" ]/g, "").replace(/u00f1/g, 'ñ').replace(/u00D1/g, 'Ñ');

                if (datos_usuario[3].replace(/[\\\[\]" ]/g, "") === "profesor") {
                    nacimiento.style.display = "none";
                    genero.style.display = "none";
                    telefono.style.display = "none";
                    nacionalidad.style.display = "none";
                    provincia.style.display = "none";
                    canton.style.display = "none";
                    distrito.style.display = "none";
                    cuenta_profesor.style.display = "block";
                    es_profesor.value = "profesor";

                    console.log(es_profesor.value);
                }
                else if (datos_usuario[3].replace(/[\\\[\]" ]/g, "") === "estudiante"){
                    nacimiento.style.display = "none";
                    genero.style.display = "none";
                    telefono.style.display = "none";
                    nacionalidad.style.display = "none";
                    provincia.style.display = "none";
                    canton.style.display = "none";
                    distrito.style.display = "none";
                    cuenta_estudiante.style.display = "block";
                    es_profesor.value = "estudiante";

                    console.log(es_profesor.value);
                }
                else if (datos_usuario[3].replace(/[\\\[\]" ]/g, "") === "prospecto"){
                    es_profesor.value = "prospecto";
                    console.log(es_profesor.value);
                }
                else if (datos_usuario[3].replace(/[\\\[\]" ]/g, "") === "estudianteprofesor"){
                    nacimiento.style.display = "none";
                    genero.style.display = "none";
                    telefono.style.display = "none";
                    nacionalidad.style.display = "none";
                    provincia.style.display = "none";
                    canton.style.display = "none";
                    distrito.style.display = "none";
                    cuenta_estudianteprofesor.style.display = "block";
                    es_profesor.value = "estudianteprofesor";
                    console.log(es_profesor.value);
                }

                nombre.readOnly = true;
                primer_apellido.readOnly = true;
                segundo_apellido.readOnly = true;

            }
        };
        xhttp.open("GET", "/obtener-datos/?identificacion=" + encodeURIComponent(input.value), true);
        xhttp.send();
    }
}
const loadingIndicator = document.getElementById('loading-indicator');
loadingIndicator.classList.remove('hidden'); // Mostrar el indicador
// Realizar la acción
loadingIndicator.classList.add('hidden'); // Ocultar el indicador
function datacarreras() {
    var select = document.getElementById("mi_select");
    select.options.length = 0; // Eliminamos todas las opciones anteriores

    fetch("/carrerasselect/").then(response => response.json()).then(data => {
        // Iteramos sobre los valores obtenidos
        data.forEach(function (valor) {
            // Creamos una nueva opción y la agregamos al select
            var opcion = document.createElement("option");
            opcion.value = valor;
            opcion.text = valor;
            select.add(opcion);
        });
    });
}