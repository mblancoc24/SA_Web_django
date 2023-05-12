$(document).ready(function () {
    var idA = document.getElementById('accesibilidadId');
    idA.onclick = function(){
        mostrar();
    }
});

function mostrar(){
    var id = document.getElementById('contentA');
    if (id.style.display !== 'none') {
        id.style.display = 'none';
    } else {
        id.style.display = 'block';
    }
}