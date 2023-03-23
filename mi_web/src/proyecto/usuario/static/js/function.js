function datacedula() {
    var input = document.getElementById("identificacion");
    if (input.value.length === 9) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var datos = this.responseText;
                console.log(datos);
                const datos_usuario = datos.split(",");

                console.log(datos_usuario[0])

                var nombre = document.getElementById("nombre");
                var primer_apellido = document.getElementById("primerapellido");
                var segundo_apellido = document.getElementById("segundoapellido");
                nombre.value = datos_usuario[0].replace(/[\\\[\]"]/g, "");
                primer_apellido.value = datos_usuario[1].replace(/[\\\[\]"]/g, "");
                segundo_apellido.value = datos_usuario[2].replace(/[\\\[\]"]/g, "");

                nombre.disabled = true;
                primer_apellido.disabled = true;
                segundo_apellido.disabled = true;
            }
        };
        xhttp.open("GET", "/obtener-datos/?cedula=" + encodeURIComponent(input.value), true);
        xhttp.send();
        
    }
}