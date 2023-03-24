function datacedula() {
    var input = document.getElementById("identificacion");
    var input2 = document.getElementById("tipo").value;
    
    if (input.value.length >= 10 && input.value.length <= 12 && input2 === "Dimex" || "Cédula Residente" || "Refugiado") {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
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
    if (input.value.length === 9 && input2 === "Cédula"){
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var datos = this.responseText;

                var nombre = document.getElementById("nombre");
                var primer_apellido = document.getElementById("primerapellido");
                var segundo_apellido = document.getElementById("segundoapellido");

                nombre.value = datos_usuario[0].replace(/[\\\[\]"]/g, "").replace(/u00f1/g, 'ñ').replace(/u00D1/g, 'Ñ');
                primer_apellido.value = datos_usuario[1].replace(/[\\\[\]" ]/g, "").replace(/u00f1/g, 'ñ').replace(/u00D1/g, 'Ñ');
                segundo_apellido.value = datos_usuario[2].replace(/[\\\[\]" ]/g, "").replace(/u00f1/g, 'ñ').replace(/u00D1/g, 'Ñ');

                nombre.readOnly = true;
                primer_apellido.readOnly = true;
                segundo_apellido.readOnly = true;
                
            }
        };
        xhttp.open("GET", "/obtener-datos/?identificacion=" + encodeURIComponent(input.value), true);
        xhttp.send();
    }
}