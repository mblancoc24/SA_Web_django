function dataHorarioEstudiante() {
    var select = document.getElementById("mi_select");
    select.options.length = 0; // Eliminamos todas las opciones anteriores

    fetch('https://mocki.io/v1/2b85b9a8-78de-4300-a691-3a55c32a05bf')
        .then(response => response.json())
        .then(data => {
            console.log(data)
    });
}