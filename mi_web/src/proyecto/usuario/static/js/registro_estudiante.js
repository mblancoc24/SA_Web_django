var provinciasCargadas = false;

function cargarProvincias() {
    if (provinciasCargadas) {
        return;
    }

    var select = document.getElementById("provincia_select");

    var url = "{% url 'obtener_provincia' %}";
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = function() {
      if (request.status === 200) {
        var data = JSON.parse(request.responseText);
        select.options.length = 0;
        for(key in data) {
          var option = document.createElement("option");
          option.value = key;
          option.text = data[key];
          select.add(option);
        }
        provinciasCargadas = true;
        dataCantones(select);
        obtenerProvincia(select)
      }
    };
    request.send();
}

function cargarCantones(valor) {
    var select = document.getElementById("canton_select");
    var select2 = document.getElementById("distrito_select");

    var url = "/obtener-canton/?provincia_select=";
    var request = new XMLHttpRequest();
    request.open('GET', url + encodeURIComponent(valor), true);
    request.onload = function() {
      if (request.status === 200) {
        var data = JSON.parse(request.responseText);
        select.options.length = 0;
        for(key in data) {
          var option = document.createElement("option");
          option.value = key;
          option.text = data[key];
          select.add(option);
        }
        dataDistritos(select)
        obtenerDistrito(select)
      }
    };
    request.send();
}

function cargarDistritos(valor1, valor2) {
    var select = document.getElementById("distrito_select");

    var url = "/obtener-distrito/?provincia_select=" + encodeURIComponent(valor1) + "&canton_select=" + encodeURIComponent(valor2);
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = function() {
      if (request.status === 200) {
        var data = JSON.parse(request.responseText);
        select.options.length = 0;
        for(key in data) {
          var option = document.createElement("option");
          option.value = key;
          option.text = data[key];
          select.add(option);
        }
        obtenerDistrito(select)
      }
    };
    request.send();
}

var paisCargadas = false;

function cargarPais() {
    if (paisCargadas) {
        return;
    }

    var select = document.getElementById("pais_select");

    select.options.length = 0; // Eliminamos todas las opciones anteriores

    var url = "{% url 'obtener_nacionalidad' %}";
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = function() {
      if (request.status === 200) {
        var data = JSON.parse(request.responseText);
        for(key in data) {
          var option = document.createElement("option");
          option.value = key;
          option.text = data[key];
          select.add(option);
        }
        paisCargadas = true;
      }
    };
    request.send();
}

function dataCantones(select){
    var valorSeleccionado = select.options[select.selectedIndex].value;
    cargarCantones(valorSeleccionado);
}

function dataDistritos(select){
    const miSelect = document.getElementById('provincia_select');
    var valorSeleccionado = select.options[select.selectedIndex].value;

    cargarDistritos(miSelect.value, valorSeleccionado);
}


function obtenerPais(select) {
    var textoSeleccionado = select.options[select.selectedIndex].text;
    document.getElementById('pais').value = textoSeleccionado;
}
function obtenerProvincia(select) {
    var textoSeleccionado = select.options[select.selectedIndex].text;
    document.getElementById('provincia').value = textoSeleccionado;
    dataCantones(select)
}
function obtenerCanton(select) {
    var textoSeleccionado = select.options[select.selectedIndex].text;
    document.getElementById('canton').value = textoSeleccionado;
    dataDistritos(select)
}
function obtenerDistrito(select) {
    var textoSeleccionado = select.options[select.selectedIndex].text;
    document.getElementById('distrito').value = textoSeleccionado;
}