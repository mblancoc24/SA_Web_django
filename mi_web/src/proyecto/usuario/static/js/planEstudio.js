$(document).ready(function () {
    const carreraSelect = document.getElementById('carrera');
    carreraSelect.onchange = function () {
        const id = document.getElementById('idP');
        const status = document.getElementById('StatusP');
        // Enviar una petición AJAX al servidor
        const url = `/prospecto/${id.textContent}/${status.textContent}/plan/carrera/`;
        const xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onload = function () {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                actualizarTabla(data);
            }
        };
        xhr.send();
    }
});

function actualizarTabla(data) {
    var estadoDiv = document.querySelector('.estado');
    var divRowPlan = document.createElement('div');
    divRowPlan.className = 'row';
    var divGrado = document.createElement('div');
    divGrado.className = 'col-md-2';
    var pGrado = document.createElement('p');
    pGrado.textContent = 'Grado: ';
    divGrado.appendChild(pGrado);

    divRowPlan.appendChild(divGrado);

    estadoDiv.appendChild(divRowPlan);

    var contenedor = document.querySelector('#mainTable');
    data.forEach((cuatrimestreObj, index) => {
        var divTablas = document.createElement('div');
        divTablas.className = 'card shadow';
        var divcard = document.createElement('div');
        var divTable = document.createElement('div');
        divTable.className = 'table-responsive tablaPlan';
        var table = document.createElement('table');
        var tituloHeader = document.createElement('h3');
        tituloHeader.className = 'mb-2';
        var titulo = document.createElement('a');
        titulo.className = 'btn-sm';
        titulo.style.border = 'none';
        titulo.style.textDecoration = 'none'
        titulo.style.color = 'black';
        titulo.style.cursor = 'pointer';
        titulo.style.transition = 'background-color 0.3s ease';
        titulo.style.borderRadius = '10px';
        titulo.addEventListener('mouseenter', function () {
            titulo.style.backgroundColor = 'rgba(0, 255, 213, 0.301)';
        });
        titulo.addEventListener('mouseleave', function () {
            titulo.style.backgroundColor = 'transparent';
        });

        titulo.onclick = function () {
            mostrarTabla(cuatrimestreObj.cuatrimestre);
        };
        titulo.textContent = cuatrimestreObj.cuatrimestre;
        tituloHeader.appendChild(titulo);
        table.className = 'table align-items-center table-flush cursoTabla';
        table.id = `${cuatrimestreObj.cuatrimestre}`;
        if (index > 1) {
            table.style.display = 'none'; // Ocultar los demás botones
            table.classList.add('tabla-oculta');
        }
        var thead = document.createElement('thead');
        var tr = document.createElement('tr');

        var th0 = document.createElement('th');
        th0.scope = "col";
        th0.appendChild(document.createTextNode('Curso'));

        var th1 = document.createElement('th');
        th1.scope = "col";
        th1.appendChild(document.createTextNode('Nombre'))

        var th2 = document.createElement('th');
        th2.scope = "col";
        th2.appendChild(document.createTextNode('Requisito'))

        var th3 = document.createElement('th');
        th3.scope = "col";
        th3.appendChild(document.createTextNode('Costo'))

        var th4 = document.createElement('th');
        th4.scope = "col";
        th4.appendChild(document.createTextNode('Creditos'))

        tr.appendChild(th0);
        tr.appendChild(th1);
        tr.appendChild(th2);
        tr.appendChild(th3);
        tr.appendChild(th4);
        thead.appendChild(tr);

        
        var col = document.createElement('div');
        col.className = 'col-md-12';
        col.appendChild(divTable);
        divTablas.appendChild(col);
        var tbody = document.createElement('tbody');
        tbody.id = 'PlanBody';
        divcard.appendChild(tituloHeader);
        divTable.appendChild(divcard);
        table.appendChild(thead);
        table.appendChild(tbody);
        divTable.appendChild(table);
        cuatrimestreObj.cursos.forEach(curso => {
            var trb = document.createElement('tr');
            trb.classList = 'principal';
            
            var icons = document.createElement('i');
            var td_siglas = document.createElement('td');
            
            td_siglas.style.width = '90px';

            if(curso.curso){
                if (curso.Aprovado){
                    icons.className = 'bi bi-check-lg';
                    icons.style.color = '#3bb80a';
                    icons.style.fontSize = '16px';
                    td_siglas.appendChild(icons);
                    td_siglas.appendChild(document.createTextNode(' '+curso.curso));
                }
                else if (curso.Matriculable){
                    icons.className = 'bi bi-plus-lg color-box';
                    icons.style.color = '#006a9f';
                    icons.style.fontSize = '16px';
                    td_siglas.appendChild(icons);
                    td_siglas.appendChild(document.createTextNode(' '+curso.curso));
                }else{ 
                    icons.className = 'bi bi-x-lg color-box';
                    icons.style.color = '#83877b';
                    td_siglas.appendChild(icons);
                    icons.style.fontSize = '16px';
                    td_siglas.appendChild(document.createTextNode(' '+curso.curso));
                }
            }

            var td_curso = document.createElement('td');
            td_curso.appendChild(document.createTextNode(curso.nombre));

            var td_requisito = document.createElement('td');
            td_requisito.appendChild(document.createTextNode(curso.requisitos));

            var td_costo = document.createElement('td');
            td_costo.appendChild(document.createTextNode('₡'+curso.tarifa));

            var td_creditos = document.createElement('td');
            td_creditos.appendChild(document.createTextNode(curso.creditos));

            trb.appendChild(td_siglas);
            trb.appendChild(td_curso);
            trb.appendChild(td_requisito);
            trb.appendChild(td_costo);
            trb.appendChild(td_creditos);

            tbody.appendChild(trb);
        });
        contenedor.appendChild(divTablas);
    });
    
}

function mostrarTabla(index) {
    const div = document.getElementById(index);
    if (div.style.display !== 'none') {
        div.style.display = 'none';
    } else {
        div.style.display = '';
    }
}