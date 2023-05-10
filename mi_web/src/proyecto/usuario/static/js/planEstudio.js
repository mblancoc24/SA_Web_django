var totalCurso;
var cursoAprovados;
var totalCreditos;
var creditosAprovados;
$(document).ready(function () {
    const carreraSelect = document.getElementById('carrera');
    carreraSelect.onchange = function () {
        totalCurso = 0;
        cursoAprovados = 0;
        totalCreditos = 0;
        creditosAprovados = 0;
        const id = document.getElementById('idP');
        const status = document.getElementById('StatusP');
        var plan = document.getElementById('carrera').value;
        // Enviar una petición AJAX al servidor
        const url = `/prospecto/${id.textContent}/${status.textContent}/plan/carrera/`;
        const xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onload = function () {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                actualizarEstado(data);
                var lineBar = new ProgressBar.Line("#line-container", {
                    trailWidth: 0.5,
                    from: { color: "#FF9900" },
                    to: { color: "#00FF99" },
                    text: {
                        value: '0',
                        className: 'progress-text',
                        style: {
                            color: 'black',
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            padding: 0,
                            margin: 0,
                            transform: 'translate(-50%, -50%)'
                        }
                    },
                    step: (state, shape) => {
                        shape.path.setAttribute("stroke", state.color);
                        shape.setText(Math.round(shape.value() * 100) + ' %');
                    }
                });
                var porcentajeAprobados = (creditosAprovados / totalCreditos) * 100;
                var procentaje = porcentajeAprobados / 100;
                lineBar.animate(procentaje, {
                    duration: 2000
                });
                actualizarTabla(data);
            }
        };
        xhr.send();
    }
});

function actualizarEstado(data) {

    data.forEach((cuatrimestreObj) => {
        totalCurso = cuatrimestreObj.data.totalCursos;;
        totalCreditos = cuatrimestreObj.data.totalCreditos;
        cursoAprovados = cuatrimestreObj.data.cursosAprobados;
        creditosAprovados = cuatrimestreObj.data.creditosAprobados;
    });
    var select = document.getElementById('carrera');
    var estadoDiv = document.querySelector('.estado');
    estadoDiv.innerHTML = '';

    var divRowPlan = document.createElement('div');
    divRowPlan.className = 'row';
    var divInfo = document.createElement('div');
    divInfo.className = 'col-md-12';

    var fieldset = document.createElement('fieldset');
    fieldset.className = 'border p-2 mb-2';
    var legend = document.createElement('legend');
    legend.className = 'float-none w-auto '
    legend.innerText = select.value;
    fieldset.appendChild(legend);

    var divRowInfo = document.createElement('div');
    divRowInfo.className = 'row';

    var divRowInfoCu = document.createElement('div');
    divRowInfoCu.className = 'row';

    var divRowInfoCr = document.createElement('div');
    divRowInfoCr.className = 'row';

    var divRowProceso = document.createElement('div');
    divRowProceso.className = 'row';

    var divGrado = document.createElement('div');
    divGrado.className = 'col-6 col-md-4';
    var pGrado = document.createElement('h6');
    pGrado.textContent = 'Grado: ' + data[0].data.grado;

    var divEnfasis = document.createElement('div');
    divEnfasis.className = 'col-6 col-md-4';
    var pEnfasis = document.createElement('h6');
    pEnfasis.textContent = 'Enfasis: ' + data[0].data.enfasis;



    divGrado.appendChild(pGrado);
    divEnfasis.appendChild(pEnfasis);
    divRowInfo.appendChild(divGrado);
    divRowInfo.appendChild(divEnfasis);

    var divCursoT = document.createElement('div');
    divCursoT.className = 'col-6 col-md-4';
    var pCursoT = document.createElement('h6');
    pCursoT.textContent = 'Total de Curso: ' + totalCurso;

    var divCursoA = document.createElement('div');
    divCursoA.className = 'col-6 col-md-4';
    var pCursoA = document.createElement('h6');
    pCursoA.textContent = 'Cursos Aprobados: ' + cursoAprovados;

    divCursoT.appendChild(pCursoT);
    divCursoA.appendChild(pCursoA);
    divRowInfoCu.appendChild(divCursoT);
    divRowInfoCu.appendChild(divCursoA);

    var divCreditoT = document.createElement('div');
    divCreditoT.className = 'col-6 col-md-4';
    var pCreditoT = document.createElement('h6');
    pCreditoT.textContent = 'Total de Créditos: ' + totalCreditos;

    var divCreditoA = document.createElement('div');
    divCreditoA.className = 'col-6 col-md-4';
    var pCreditoA = document.createElement('h6');
    pCreditoA.textContent = 'Créditos Aprobados: ' + creditosAprovados;

    divCreditoT.appendChild(pCreditoT);
    divCreditoA.appendChild(pCreditoA);
    divRowInfoCr.appendChild(divCreditoT);
    divRowInfoCr.appendChild(divCreditoA);

    var divproceso = document.createElement('div');
    divproceso.className = 'col-md-12';
    var pProceso = document.createElement('h6');
    pProceso.textContent = 'Total Completado';
    var divEstado = document.createElement('div');
    divEstado.id = 'line-container';

    divproceso.appendChild(pProceso);
    divproceso.appendChild(divEstado);
    divRowProceso.appendChild(divproceso);

    fieldset.appendChild(divRowInfo);
    fieldset.appendChild(divRowInfoCu);
    fieldset.appendChild(divRowInfoCr);
    fieldset.appendChild(divRowProceso);

    divInfo.appendChild(fieldset);

    divRowPlan.appendChild(divInfo);

    estadoDiv.appendChild(divRowPlan);
}

function actualizarTabla(data) {
    var contenedor = document.querySelector('#mainTable');
    contenedor.innerHTML = '';
    data.forEach(cuatrimestreObj => {
        var mallaCurricular = cuatrimestreObj.data.mallaCurricular;
        const cursosAprobados = data[0].data.cursosAprobadosCodigos.map(curso => curso.codigo);
        console.log(cursosAprobados)
        mallaCurricular.forEach((curso, index) => {
           
            var divTablas = document.createElement('div');
            divTablas.className = 'card shadow';

            var divCardheader = document.createElement('div');
            divCardheader.className = 'card-header';
            var divCardBody = document.createElement('div');
            divCardBody.className = 'card-body table-responsive p-0 tablaPlan';
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
                mostrarTabla(curso.cuatrimestre);
            };
            titulo.textContent = curso.cuatrimestre;
            tituloHeader.appendChild(titulo);
            var table = document.createElement('table');
            table.className = 'table align-items-center table-flush cursoTabla';
            table.id = `${curso.cuatrimestre}`;
            if (index > 1) {
                table.style.display = 'none'; // Ocultar los demás botones
                table.classList.add('tabla-oculta');
            }
            var thead = document.createElement('thead');
            var tr = document.createElement('tr');

            var thAp = document.createElement('th');
            thAp.scope = "col";
            thAp.style.width = '10px';

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
            th3.appendChild(document.createTextNode('Creditos'))

            tr.appendChild(thAp);
            tr.appendChild(th0);
            tr.appendChild(th1);
            tr.appendChild(th2);
            tr.appendChild(th3);
            thead.appendChild(tr);
            var tbody = document.createElement('tbody');
            tbody.id = 'PlanBody';
            divCardheader.appendChild(tituloHeader);
            table.appendChild(thead);
            table.appendChild(tbody);
            divTablas.appendChild(divCardheader);
            divCardBody.appendChild(table);
            divTablas.appendChild(divCardBody);
            curso.cursos.forEach(items => {
                if (items.curso !== '') {
                    var trb = document.createElement('tr');
                    trb.classList = 'principal';
                    var icons = document.createElement('i');
                    var td_apro = document.createElement('td');
                    td_apro.style.width = '10px';
                    if(cursosAprobados.includes(items.curso)){
                        icons.className = 'bi bi-check-lg';
                        icons.style.color = '#3bb80a';
                        icons.style.fontSize = '16px';
                        td_apro.appendChild(icons);
                    }else if(items.requisitos === ''){
                        icons.className = 'bi bi-plus-lg color-box';
                        icons.style.color = '#006a9f';
                        icons.style.fontSize = '16px';
                        td_apro.appendChild(icons);
                    } else if (items.requisitos.split(',').every(requisito => cursosAprobados.includes(requisito))) {
                        icons.className = 'bi bi-plus-lg color-box';
                        icons.style.color = '#006a9f';
                        icons.style.fontSize = '16px';
                        td_apro.appendChild(icons);
                    }else{
                        icons.className = 'bi bi-x-lg color-box';
                        icons.style.color = '#83877b';
                        icons.style.fontSize = '16px';
                        td_apro.appendChild(icons);
                    }
                    var td_siglas = document.createElement('td');
                    var td_curso = document.createElement('td');
                    var td_requisito = document.createElement('td');
                    var td_creditos = document.createElement('td');
                    td_siglas.appendChild(document.createTextNode(' ' + items.curso));
                    td_curso.appendChild(document.createTextNode(items.nombre));
                    td_requisito.appendChild(document.createTextNode(items.requisitos));
                    td_creditos.appendChild(document.createTextNode(items.creditos));
                    trb.appendChild(td_apro);
                    trb.appendChild(td_siglas);
                    trb.appendChild(td_curso);
                    trb.appendChild(td_requisito);
                    trb.appendChild(td_creditos);
                    tbody.appendChild(trb);
                }

            });
            contenedor.appendChild(divTablas);
        });
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