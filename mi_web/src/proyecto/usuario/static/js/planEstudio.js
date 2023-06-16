var totalCurso;
var cursoAprovados;
var totalCreditos;
var creditosAprovados;
var cursoPre = [];
var horariosCurso = [];
var cantidadCursos;
var auxCantCursos;
$(document).ready(function () {
    const type = document.getElementById('typeE');
    const id = document.getElementById('idE');
    const status = document.getElementById('StatusE');
    var botonPrematricula = document.getElementById('prematriculaBtn');
    botonPrematricula.onclick = function () {
        mostrarPrematricula();
    }
    const carreraSelect = document.getElementById('carrera');
    carreraSelect.onchange = function () {
        totalCurso = 0;
        cursoAprovados = 0;
        totalCreditos = 0;
        creditosAprovados = 0;

        var plan = document.getElementById('carrera').value;
        // Enviar una petición AJAX al servidor
        //const url = `/prospecto/${id.textContent}/${status.textContent}/plan/carrera/?carrera=` + encodeURIComponent(plan);
        const url = `/${type.textContent}/${id.textContent}/${status.textContent}/plan/carrera/`;
        const xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
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
    var botonEnviarPrematricula = document.getElementById('enviarPrematricula');
    botonEnviarPrematricula.onclick = function () {
        enviarPrematricula(id.textContent);
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
    divInfo.className = 'col-12 col-md-12';

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
        cantidadCursos = cuatrimestreObj.data.recargo;
        auxCantCursos = cuatrimestreObj.data.recargo;
        var mallaCurricular = cuatrimestreObj.data.mallaCurricular;
        const cursosAprobados = data[0].data.cursosAprobadosCodigos.map(curso => curso.codigo);
        mallaCurricular.forEach((curso, index) => {

            var divTablas = document.createElement('div');
            divTablas.className = 'card shadow p-2';

            var divCardheader = document.createElement('div');
            divCardheader.className = 'card-header border-0 py-0';
            divCardheader.id = 'planHeader';
            var divCardBody = document.createElement('div');
            divCardBody.className = 'card-body table-responsive p-0 tablaPlan  mt-2';
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
            thAp.className = 'd-none d-sm-table-cell';
            thAp.style.width = '10px';

            var th0 = document.createElement('th');
            th0.scope = "col";
            th0.appendChild(document.createTextNode('Curso'));

            var th1 = document.createElement('th');
            th1.scope = "col";
            th1.appendChild(document.createTextNode('Nombre'));

            var th2 = document.createElement('th');
            th2.scope = "col";
            th2.className = 'd-none d-sm-table-cell';
            th2.appendChild(document.createTextNode('Requisito'));

            var th3 = document.createElement('th');
            th3.scope = "col";
            th3.className = 'd-none d-sm-table-cell';
            th3.appendChild(document.createTextNode('Creditos'));

            var th4 = document.createElement('th');
            th4.scope = "col";
            var iconTh4 = document.createElement('i');
            iconTh4.className = 'bi bi-clipboard';
            th4.appendChild(iconTh4);

            var th5 = document.createElement('th');
            th5.scope = "col";
            var iconTh5 = document.createElement('i');
            iconTh5.className = 'bi bi-gear';
            th5.appendChild(iconTh5);

            tr.appendChild(thAp);
            tr.appendChild(th0);
            tr.appendChild(th1);
            tr.appendChild(th2);
            tr.appendChild(th3);
            tr.appendChild(th4);
            tr.appendChild(th5);
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
                    td_apro.className = 'd-none d-sm-table-cell';
                    td_apro.style.width = '10px';
                    var checkOpcion = document.createElement('input');
                    checkOpcion.type = 'checkbox';
                    checkOpcion.id = `${items.curso}-checkbox`;
                    var btnLevantamiento = document.createElement('a');
                    btnLevantamiento.className = 'link-info link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover';
                    btnLevantamiento.onclick = function () {
                        actualizarModal(items.curso);
                    }
                    var dots = document.createElement('i');
                    dots.className = 'bi bi-three-dots-vertical';
                    btnLevantamiento.appendChild(dots);
                    var td_gest = document.createElement('td');
                    if (cursosAprobados.includes(items.curso)) {
                        trb.id = 'aprovado';

                        icons.className = 'bi bi-check-lg';
                        icons.style.color = '#3bb80a';
                        icons.style.fontSize = '16px';
                        checkOpcion.setAttribute("hidden", true);
                        td_apro.appendChild(icons);
                    } else if (items.requisitos === '') {
                        icons.className = 'bi bi-plus-lg color-box';
                        trb.id = 'matriculable';
                        icons.style.color = '#006a9f';
                        icons.style.fontSize = '16px';
                        td_apro.appendChild(icons);
                    } else if (items.requisitos.split(',').every(requisito => cursosAprobados.includes(requisito))) {
                        icons.className = 'bi bi-plus-lg color-box';
                        trb.id = 'matriculable';
                        icons.style.color = '#006a9f';
                        icons.style.fontSize = '16px';
                        td_apro.appendChild(icons);
                    } else {
                        icons.className = 'bi bi-x-lg color-box';
                        trb.id = 'noMatriculable';
                        icons.style.color = '#83877b';
                        icons.style.fontSize = '16px';
                        checkOpcion.setAttribute("hidden", true);
                        td_gest.appendChild(btnLevantamiento);
                        td_apro.appendChild(icons);
                    }
                    var td_pre = document.createElement('td');
                    var td_siglas = document.createElement('td');
                    var td_curso = document.createElement('td');
                    var td_requisito = document.createElement('td');
                    td_requisito.className = 'd-none d-sm-table-cell';
                    var td_creditos = document.createElement('td');
                    td_creditos.className = 'd-none d-sm-table-cell';
                    td_siglas.appendChild(document.createTextNode(' ' + items.curso));
                    td_curso.appendChild(document.createTextNode(items.nombre));
                    td_requisito.appendChild(document.createTextNode(items.requisitos));
                    td_creditos.appendChild(document.createTextNode(items.creditos));
                    checkOpcion.onchange = function () {
                        visualizar(items.curso, items.nombre, items.creditos, `${items.curso}-checkbox`);
                    }
                    td_pre.appendChild(checkOpcion);
                    trb.appendChild(td_apro);
                    trb.appendChild(td_siglas);
                    trb.appendChild(td_curso);
                    trb.appendChild(td_requisito);
                    trb.appendChild(td_creditos);
                    trb.appendChild(td_pre);
                    trb.appendChild(td_gest);
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

function visualizar(curso, nombre, creditos, id) {
    const prematriculaOption = document.querySelector('#opcionPrematricula');
    const cursoObj = {
        curso: curso,
        nombre: nombre,
        creditos: creditos,
    };
    prematriculaOption.style.display = '';
    var checkBox = document.getElementById(id);
    var toast = document.querySelector('#liveToast');
    var content = document.getElementById('toastContent');
    console.log(cantidadCursos);
    if (checkBox.checked && cantidadCursos > 0) {
        cursoPre.push(cursoObj);
        horariosCurso.push(curso);
        cantidadCursos -= 1;
        var cursos = document.getElementById('cantCursos');
        var auxCu = parseInt(cursos.innerText);
        var totalCu = auxCu + 1;
        cursos.innerText = totalCu;
    } else if (!checkBox.checked) {
        cursoPre.splice(cursoPre.indexOf(curso), 1);
        cantidadCursos += 1;
        var cursos = document.getElementById('cantCursos');
        var auxCu = parseInt(cursos.innerText);
        var totalCu = auxCu - 1;
        cursos.innerText = totalCu;
    } else {
        content.innerText = `Solo puede prematricular ${auxCantCursos} cursos`;
        checkBox.checked = false;
        var toast = new bootstrap.Toast(toast, { delay: 3000 });
        toast.show();
    }
}

function mostrarPrematricula() {
    var tbodyModal = document.getElementById('premTablaBody');
    var count = 0;
    tbodyModal.innerHTML = '';

    cursoPre.forEach(curso => {
        var trTablaModal = document.createElement('tr');
        trTablaModal.id = `${curso.curso}-fila`;
        trTablaModal.className = 'border-bottom';
        var tdCheckModal = document.createElement('td');
        var divCheckModal = document.createElement('div');
        var checkTablaModal = document.createElement('input');
        checkTablaModal.type = 'checkbox';
        checkTablaModal.checked = 'true';
        checkTablaModal.id = `${curso.curso}-preCheckModal`;
        checkTablaModal.onchange = function () {
            quitarPrematricula(`${curso.curso}-fila`, `${curso.curso}-checkbox`, curso.creditos);
        }
        divCheckModal.className = 'd-flex align-items-center justify-content-center';
        divCheckModal.appendChild(checkTablaModal);

        var tdSiglaModal = document.createElement('td');
        var divSiglaModal = document.createElement('div');
        var spanSiglaModal = document.createElement('span');
        divSiglaModal.className = 'd-flex align-items-center justify-content-center';
        spanSiglaModal.className = 'pe-3 fw-normal';
        spanSiglaModal.id = 'siglasCursos';
        spanSiglaModal.innerText = curso.curso;
        divSiglaModal.appendChild(spanSiglaModal);

        var tdNombreModal = document.createElement('td');
        var divNombreModal = document.createElement('div');
        var divNombrePModal = document.createElement('div');
        var pNombreModal = document.createElement('p');
        divNombreModal.className = 'd-flex align-items-center';
        divNombrePModal.className = 'ps-3 d-flex flex-column justify-content';
        pNombreModal.className = 'fw-normal';
        pNombreModal.innerText = curso.nombre;
        divNombrePModal.appendChild(pNombreModal);
        divNombreModal.appendChild(divNombrePModal);

        var tdCreditoModal = document.createElement('td');
        var divCreditoModal = document.createElement('div');
        var pCreditoModal = document.createElement('p');
        var spanCreditoModal = document.createElement('span');
        divCreditoModal.className = 'd-flex align-items-center justify-content-center';
        pCreditoModal.className = 'pe-3';
        spanCreditoModal.className = 'red';
        spanCreditoModal.innerText = curso.creditos;
        pCreditoModal.appendChild(spanCreditoModal);
        divCreditoModal.appendChild(spanCreditoModal);

        var tdSelectModal = document.createElement('td');
        var divSelectModal = document.createElement('div');
        var selectTablaModal = document.createElement('select');
        var optionTablaSelectModal = document.createElement('option');
        optionTablaSelectModal.setAttribute('disabled', true);
        optionTablaSelectModal.setAttribute('selected', true);
        optionTablaSelectModal.setAttribute('value', '');
        optionTablaSelectModal.setAttribute('hidden', true);
        optionTablaSelectModal.innerText = 'Horarios';
        selectTablaModal.id = `${curso.curso}-horarios`;
        selectTablaModal.appendChild(optionTablaSelectModal);
        selectTablaModal.className = 'form-select form-select-sm';
        divSelectModal.className = 'd-flex align-items-center justify-content-center';
        divSelectModal.appendChild(selectTablaModal);

        tdCheckModal.appendChild(divCheckModal);
        tdSiglaModal.appendChild(divSiglaModal);
        tdNombreModal.appendChild(divNombreModal);
        tdCreditoModal.appendChild(divCreditoModal);
        tdSelectModal.appendChild(divSelectModal);

        trTablaModal.appendChild(tdCheckModal);
        trTablaModal.appendChild(tdSiglaModal);
        trTablaModal.appendChild(tdNombreModal);
        trTablaModal.appendChild(tdCreditoModal);
        trTablaModal.appendChild(tdSelectModal);
        count += curso.creditos;
        tbodyModal.appendChild(trTablaModal);
    });
    var trTotal = document.createElement('tr');
    trTotal.className = 'border-bottom';
    var tdTotalModal = document.createElement('td');
    tdTotalModal.colSpan = '4'
    var divTotalModal = document.createElement('div');
    var spanTotalModal = document.createElement('span');
    divTotalModal.className = 'd-flex align-items-center justify-content-end';
    spanTotalModal.className = 'pe-3 fw-normal';
    spanTotalModal.innerText = `Total de Creditos: ${count}`;
    spanTotalModal.id = 'totalCreditos';
    divTotalModal.appendChild(spanTotalModal);
    tdTotalModal.appendChild(divTotalModal);
    trTotal.appendChild(tdTotalModal);

    tbodyModal.appendChild(trTotal);
    const id = document.getElementById('idE');
    const status = document.getElementById('StatusE');
    const type = document.getElementById('typeE');
    const url = `/${type.textContent}/${id.textContent}/${status.textContent}/plan/cursoPlanHorario/` + "?cursos=" + encodeURIComponent(horariosCurso);
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            getHorarios(data);
        }
    };
    xhr.send();
}

function quitarPrematricula(fila, checkId, credito) {
    var totalCreditos = document.getElementById('totalCreditos');
    var auxTotal = totalCreditos.innerText.split(': ');
    var totalCr = auxTotal[1] - credito;
    totalCreditos.innerText = `Total de Creditos: ${totalCr}`;
    var cursos = document.getElementById('cantCursos');
    var filaTablaModal = document.getElementById(fila);
    filaTablaModal.parentNode.removeChild(filaTablaModal);
    var checkBoxTabla = document.getElementById(checkId);
    console.log(checkBoxTabla);
    checkBoxTabla.checked = false;
    var auxCu = parseInt(cursos.innerText);
    var totalCu = auxCu - 1;
    cursos.innerText = totalCu;
    cantidadCursos += 1;

    for (var i = 0; i < cursoPre.length; i++) {
        if (`${cursoPre[i].curso}-fila` === fila) {
            cursoPre.splice(i, 1);
            break;
        }
    }
}

function enviarPrematricula(id) {
    var tabla = document.getElementById("premTablaBody");
    var identificacion = document.getElementById('idE');
    var status = document.getElementById('StatusE');
    var type = document.getElementById('typeE');
    var cursos = [];
    for (var i = 0; i < tabla.rows.length - 1; i++) {
        var fila = tabla.rows[i];
        var siglasCurso = fila.querySelector("#siglasCursos").textContent;
        var horarioSelect = fila.querySelector("select").value;
        var curso = {
            "curso": siglasCurso,
            "horario": horarioSelect
        };
        cursos.push(curso);
    }
    var jsonData = {
        "identificacion": "604150895",
        "cursos": cursos
    };
    var jsonString = JSON.stringify(jsonData);
    console.log(jsonString);
    var xhr = new XMLHttpRequest();
    var url = `/${type.textContent}/${identificacion.textContent}/${status.textContent}/plan/envioPrematricula/`;
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    
    // Include the CSRF token in the request headers
    var csrfToken = getCSRFToken(); // Replace with the actual function to get the CSRF token
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // The request was completed successfully
            var response = JSON.parse(xhr.responseText);
            console.log(response);
            // Perform necessary actions with the server response
        }
    };
    xhr.send(jsonString);
}

function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Extract the CSRF token from the cookie
        if (cookie.substring(0, 'csrftoken'.length + 1) === 'csrftoken=') {
          cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

function actualizarModal(curso) {

    var cursoModal = document.getElementById('cursoModal');
    cursoModal.value = curso;
    $('#modal_levantamiento').modal('show');
}

function getHorarios(data) {
    var siglas = document.querySelectorAll('#siglasCursos');
    data.forEach((horarios) => {
        var horariosCurso = horarios.data.horarios;
        horariosCurso.forEach(curso => {
            siglas.forEach(function (elemento) {
                if (elemento.textContent === curso.curso) {
                    var selectId = document.getElementById(`${elemento.textContent}-horarios`);
                    curso.horarios.forEach(horario => {
                        var opcionSelect = document.createElement('option');
                        opcionSelect.setAttribute('value', horario);
                        opcionSelect.innerText = horario;
                        selectId.appendChild(opcionSelect);
                    });
                }
            });
        });
    });
}