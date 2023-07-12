function getPeriodo() {
    const url = '/getCurso/';
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            detalle(data);
        }
    };
    xhr.send();
}
function detalle(data) {
    var selectedPeriodo = document.getElementById('periodos').value;
    var cardsContainer = document.getElementById('cardsContainer');
    cardsContainer.innerHTML = '';

    var cursos = {};

    for (var i = 0; i < data.data.periodos.length; i++) {
        var periodo = data.data.periodos[i];
        if (periodo.periodo === selectedPeriodo) {
            for (var j = 0; j < periodo.horarios.length; j++) {
                var horario = periodo.horarios[j];
                if (!cursos.hasOwnProperty(horario.curso)) {
                    cursos[horario.curso] = {
                        curso: horario.curso,
                        horarios: []
                    };
                }
                cursos[horario.curso].horarios.push(horario);
            }
        }
    }

    for (var cursoKey in cursos) {
        if (cursos.hasOwnProperty(cursoKey)) {
            var curso = cursos[cursoKey];

            // Crear el card
            var card = document.createElement('div');
            card.className = 'card mb-4 mt-1';

            // Crear el título del card
            var cardTitle = document.createElement('h1');
            cardTitle.className = 'card-title p-2 fw-bold';
            cardTitle.textContent = curso.curso;

            // Crear el header del card
            var cardHeader = document.createElement('div');
            cardHeader.className = 'card-header';

            // Crear la lista de pestañas en el header
            var tabList = document.createElement('ul');
            tabList.className = 'nav nav-tabs card-header-tabs';
            tabList.role = 'tablist';
            tabList.id = 'v-pills-tab';

            // Crear las pestañas de los subhorarios
            for (var k = 0; k < curso.horarios.length; k++) {
                var subhorario = curso.horarios[k];
                var tabItem = document.createElement('li');
                tabItem.className = 'nav-item';

                var tabLink = document.createElement('a');
                tabLink.className = subhorario === curso.horarios[0] ? 'nav-link active' : 'nav-link';
                tabLink.href = '#curso' + (k + 1);
                tabLink.setAttribute('data-bs-toggle', 'pill');
                tabLink.textContent = subhorario.horario;

                tabItem.appendChild(tabLink);
                tabList.appendChild(tabItem);
            }

            cardHeader.appendChild(tabList);

            // Crear el cuerpo del card
            var cardBody = document.createElement('div');
            cardBody.className = 'card-body';

            // Crear el contenedor de las pestañas en el cuerpo
            var tabContent = document.createElement('div');
            tabContent.className = 'tab-content';
            tabContent.id = 'v-pills-tabContent';

            // Crear las pestañas de los subhorarios en el cuerpo
            for (var k = 0; k < curso.horarios.length; k++) {
                var subhorarioAux = curso.horarios[k];
                var tabPane = document.createElement('div');
                tabPane.className = subhorarioAux === curso.horarios[0] ? 'tab-pane fade show active mb-3' : 'tab-pane fade show mb-3';
                tabPane.id = 'curso' + (k + 1);
                tabPane.role = 'tabpanel';
                tabPane.setAttribute('aria-labelledby', 'v-pills-home-tab');

                // Crear la tabla dentro de la pestaña
                var table = document.createElement('table');
                table.className = 'table misCursoTabla';

                // Crear las filas de la tabla
                var tbody = document.createElement('tbody');

                var tr1 = document.createElement('tr');
                var td11 = document.createElement('td');
                td11.id = 'datos';
                td11.style.width = '50px';
                td11.textContent = 'Periodo:';
                var td12 = document.createElement('td');
                td12.colSpan = '6';
                td12.style.width = '50px';
                td12.textContent = subhorarioAux.periodo;
                tr1.appendChild(td11);
                tr1.appendChild(td12);

                var tr2 = document.createElement('tr');
                var td21 = document.createElement('td');
                td21.id = 'datos';
                td21.style.width = '50px';
                td21.textContent = 'Sede:';
                var td22 = document.createElement('td');
                td22.style.width = '50px';
                td22.textContent = subhorarioAux.sede;
                var td23 = document.createElement('td');
                td23.id = 'datos';
                td23.style.width = '50px';
                td23.textContent = '# Grupo:';
                var td24 = document.createElement('td');
                td24.style.width = '50px';
                td24.textContent = subhorarioAux.grupo;
                var td25 = document.createElement('td');
                td25.id = 'datos';
                td25.style.width = '50px';
                td25.textContent = 'Aula:';
                var td26 = document.createElement('td');
                td26.style.width = '50px';
                td26.textContent = subhorarioAux.aula;
                tr2.appendChild(td21);
                tr2.appendChild(td22);
                tr2.appendChild(td23);
                tr2.appendChild(td24);
                tr2.appendChild(td25);
                tr2.appendChild(td26);

                var tr3 = document.createElement('tr');
                var td27 = document.createElement('td');
                td27.id = 'datos';
                td27.style.width = '50px';
                td27.textContent = 'Horario:';
                var td28 = document.createElement('td');
                td28.style.width = '50px';
                td28.textContent = subhorarioAux.horario;
                var td29 = document.createElement('td');
                td29.id = 'datos';
                td29.style.width = '50px';
                td29.textContent = 'Estado:';
                var td30 = document.createElement('td');
                td30.style.width = '50px';
                td30.textContent = subhorarioAux.estado;
                td30.colSpan = '3';
                tr3.appendChild(td27);
                tr3.appendChild(td28);
                tr3.appendChild(td29);
                tr3.appendChild(td30);

                var tr4 = document.createElement('tr');
                var td31 = document.createElement('td');
                td31.id = 'datos';
                td31.style.width = '50px';
                td31.textContent = 'Cupo:';
                var td32 = document.createElement('td');
                td32.style.width = '50px';
                td32.textContent = subhorarioAux.cupo;
                var td33 = document.createElement('td');
                td33.id = 'datos';
                td33.style.width = '50px';
                td33.textContent = 'Matricula:';
                var td34 = document.createElement('td');
                td34.style.width = '50px';
                td34.textContent = subhorarioAux.matricula;
                td34.colSpan = '3';
                tr4.appendChild(td31);
                tr4.appendChild(td32);
                tr4.appendChild(td33);
                tr4.appendChild(td34);

                var tr5 = document.createElement('tr');
                var td35 = document.createElement('td');
                td35.id = 'datos';
                td35.style.width = '50px';
                td35.textContent = 'Entrega Notas:';
                var td36 = document.createElement('td');
                td36.colSpan = '5';
                td36.style.width = '50px';
                td36.textContent = subhorarioAux.entregaNotas;
                tr5.appendChild(td35);
                tr5.appendChild(td36);
                // ... Código HTML para las filas ...

                tbody.appendChild(tr1);
                tbody.appendChild(tr2);
                tbody.appendChild(tr3);
                tbody.appendChild(tr4);
                tbody.appendChild(tr5);

                // ... Agregar las demás filas a tbody ...

                table.appendChild(tbody);

                // Agregar la tabla al contenedor
                var tableContainer = document.createElement('div');
                tableContainer.className = 'table-responsive mb-3';
                tableContainer.appendChild(table);
                tabPane.appendChild(tableContainer);

                // ... Código HTML para los botones ...
                var divbutton0 = document.createElement('div');
                divbutton0.className = 'btn-group mr-2';
                divbutton0.role = 'group';
                var btnEstudiantes = document.createElement('button');
                btnEstudiantes.className = 'btn btn-secondary';
                btnEstudiantes.type = 'button';
                btnEstudiantes.textContent = 'Ver estudiantes';
                // Agregar lógica de clic al botón de estudiante
                btnEstudiantes.addEventListener('click', function () {
                    // Lógica para el botón de estudiante
                    listaEstudiante();
                });
                divbutton0.appendChild(btnEstudiantes);
                tabPane.appendChild(divbutton0);
                if (subhorarioAux.asistencia) {
                    var divbutton1 = document.createElement('div');
                    divbutton1.className = 'btn-group mr-2';
                    divbutton1.role = 'group';
                    var btnAsistencia = document.createElement('button');
                    btnAsistencia.className = 'btn btn-secondary';
                    btnAsistencia.type = 'button';
                    btnAsistencia.textContent = 'Asistencia';
                    // Agregar lógica de clic al botón de asistencia
                    btnAsistencia.addEventListener('click', function () {
                        // Lógica para el botón de asistencia
                        asistencia('2023-05-15', '2023-08-22');
                    });
                    divbutton1.appendChild(btnAsistencia);
                    tabPane.appendChild(divbutton1);
                }

                if (subhorarioAux.nota) {
                    var divbutton2 = document.createElement('div');
                    divbutton2.className = 'btn-group mr-2';
                    divbutton2.role = 'group';
                    var btnNota = document.createElement('button');
                    btnNota.className = 'btn btn-secondary';
                    btnNota.type = 'button';
                    btnNota.textContent = 'Nota';
                    // Agregar lógica de clic al botón de nota
                    btnNota.id = 'nota' + cursoKey + k;
                    btnNota.addEventListener('click', function (event) {
                        // Lógica para el botón de nota
                        const botonId = event.target.id;
                        notas('Estudiantes' + botonId, botonId);
                    });
                    divbutton2.appendChild(btnNota);
                    tabPane.appendChild(divbutton2);
                }

                if (subhorarioAux.actas) {
                    var divbutton3 = document.createElement('div');
                    divbutton3.className = 'btn-group mr-2';
                    divbutton3.role = 'group';
                    var btnActas = document.createElement('button');
                    btnActas.className = 'btn btn-secondary';
                    btnActas.type = 'button';
                    btnActas.textContent = 'Actas';
                    // Agregar lógica de clic al botón de actas
                    btnActas.addEventListener('click', function () {
                        // Lógica para el botón de actas
                        console.log('Clic en el botón de actas');
                    });
                    divbutton3.appendChild(btnActas);
                    tabPane.appendChild(divbutton3);
                }
                tabContent.appendChild(tabPane);
            }

            cardBody.appendChild(tabContent);
            card.appendChild(cardTitle);
            card.appendChild(cardHeader);
            card.appendChild(cardBody);

            // Agregar el card al contenedor de cards
            cardsContainer.appendChild(card);
        }
    }
}

function getData() {
    return new Promise(function (resolve, reject) {
        const url = '/getListaEstudiantes/';
        const xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onload = function () {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                resolve(data);
            } else {
                reject(xhr.statusText);
            }
        }
        xhr.onerror = function () {
            reject(xhr.statusText);
        }
        xhr.send();
    });
}

function listaEstudiante() {
    getData()
        .then(function (dataL) {
            var data = dataL;
            var contenedor = document.querySelector('#modal_funcionesBody');
            contenedor.innerHTML = '';
            document.getElementById('modal_funcionesTitle').innerText = 'Lista de Estudiantes'
            var divTable = document.createElement('div');
            divTable.className = 'table-responsive-lg mb-3';

            var table = document.createElement('table');
            table.className = 'table table-striped table-bordered dataTable';
            table.id = 'tablaLista';

            var thead = document.createElement('thead');
            var tr = document.createElement('tr');

            var thC = document.createElement('th');
            thC.scope = "col";
            thC.appendChild(document.createTextNode('Identificación'));

            var thN = document.createElement('th');
            thN.scope = "col";
            thN.appendChild(document.createTextNode('Nombre'));

            var thCo = document.createElement('th');
            thCo.scope = "col";
            thCo.appendChild(document.createTextNode('Correo'));

            var thT1 = document.createElement('th');
            thT1.scope = "col";
            thT1.appendChild(document.createTextNode('Telefono 1'));

            var thT2 = document.createElement('th');
            thT2.scope = "col";
            thT2.appendChild(document.createTextNode('Telefono 2'));
            tr.appendChild(thC);
            tr.appendChild(thN);
            tr.appendChild(thCo);
            tr.appendChild(thT1);
            tr.appendChild(thT2);
            thead.appendChild(tr);
            table.appendChild(thead);
            var tbody = document.createElement('tbody');
            tbody.id = 'listBody';
            table.appendChild(tbody);
            data.forEach(estudiante => {
                var trb = document.createElement('tr');
                var td_C = document.createElement('td');
                td_C.appendChild(document.createTextNode(' ' + estudiante.carné));

                var td_N = document.createElement('td');
                td_N.appendChild(document.createTextNode(' ' + estudiante.nombre));

                var td_Co = document.createElement('td');
                td_Co.appendChild(document.createTextNode(' ' + estudiante.correo));

                var td_T1 = document.createElement('td');
                td_T1.appendChild(document.createTextNode(' ' + estudiante.telefono1));

                var td_T2 = document.createElement('td');
                td_T2.appendChild(document.createTextNode(' ' + estudiante.telefono2));

                trb.appendChild(td_C);
                trb.appendChild(td_N);
                trb.appendChild(td_Co);
                trb.appendChild(td_T1);
                trb.appendChild(td_T2);
                tbody.appendChild(trb);
            });

            divTable.appendChild(table);
            contenedor.appendChild(divTable);
            $('#tablaLista').DataTable({
                language: {
                    "sLengthMenu": "Mostrar _MENU_ registros",
                    "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                    "sZeroRecords": "No se encontraron resultados",
                    "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                    "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                    "sSearch": "Buscar:",
                    "oPaginate": {
                        "sFirst": "Primero",
                        "sLast": "Último",
                        "sNext": "Siguiente",
                        "sPrevious": "Anterior"
                    },
                }

            });

            $('#modal_funciones').modal('show');
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
}

function getSemanas(date1, date2) {
    var fechaInicio = new Date(date1);
    var fechaFin = new Date(date2);
    var diferencia = fechaFin.getTime() - fechaInicio.getTime();
    var semanas = Math.ceil(diferencia / (1000 * 60 * 60 * 24 * 7));
    var semanasList = [];
    for (var i = 1; i <= semanas; i++) {
        semanasList.push(i);
    }
    return semanasList;
}

function asistencia(date1, date2) {
    var lista = getSemanas(date1, date2);
    var contenedor = document.querySelector('#modal_funcionesBody');
    contenedor.innerHTML = '';
    document.getElementById('modal_funcionesTitle').innerText = 'Asistencia'
    var divRow = document.createElement('div');
    divRow.className = 'row';
    var divSelect = document.createElement('div');
    divSelect.className = 'form-group col-12 col-lg-3 col-md-6 col-sm-12 mx-auto';
    var label = document.createElement('label');
    label.className = '';
    label.setAttribute('for', 'semana');
    label.innerText = 'Seleccione una semana'
    var select = document.createElement('select');
    select.className = 'form-select';
    select.id = 'selectSemana';
    var optionD = document.createElement('option');
    optionD.selected = true;
    optionD.disabled = true;
    optionD.hidden = true;
    optionD.innerText = 'Seleccione una semana'
    select.appendChild(optionD);
    lista.forEach(item => {
        var option = document.createElement('option');
        option.value = item;
        option.innerText = item;
        select.appendChild(option);
    })
    divSelect.appendChild(label);
    select.addEventListener('change', function () {
        var divTable = document.querySelector('#divTable');
        if (divTable) {
            divTable.remove();
        }
        updateTabla();
    });
    divSelect.appendChild(select);
    divRow.appendChild(divSelect);
    contenedor.appendChild(divRow);
    $('#modal_funciones').modal('show');
}

function updateTabla() {
    getData()
        .then(function (dataL) {
            var data = dataL;
            var divTable = document.createElement('div');
            divTable.className = 'table-responsive-lg mb-3';
            divTable.id = 'divTable';
            var table = document.createElement('table');
            table.className = 'table table-striped table-bordered dataTable';
            table.id = 'tablaLista';

            var thead = document.createElement('thead');
            var tr = document.createElement('tr');

            var thNu = document.createElement('th');
            thNu.scope = "col";
            thNu.appendChild(document.createTextNode('#'));

            var thC = document.createElement('th');
            thC.scope = "col";
            thC.appendChild(document.createTextNode('Identificación'));

            var thN = document.createElement('th');
            thN.scope = "col";
            thN.appendChild(document.createTextNode('Nombre'));

            var thP = document.createElement('th');
            thP.scope = "col";
            thP.appendChild(document.createTextNode('Presente'));

            tr.appendChild(thNu);
            tr.appendChild(thC);
            tr.appendChild(thN);
            tr.appendChild(thP);

            thead.appendChild(tr);
            table.appendChild(thead);
            var tbody = document.createElement('tbody');
            tbody.id = 'listBody';
            table.appendChild(tbody);
            divTable.appendChild(table);

            data.forEach((estudiante, item) => {
                var trRow = document.createElement('tr');
                var td_Nu = document.createElement('td');
                var pos = item + 1
                td_Nu.appendChild(document.createTextNode(' ' + pos));

                var td_I = document.createElement('td');
                td_I.appendChild(document.createTextNode(' ' + estudiante.carné));

                var td_No = document.createElement('td');
                td_No.appendChild(document.createTextNode(' ' + estudiante.nombre));

                var checkOpcion = document.createElement('input');
                checkOpcion.type = 'checkbox';
                checkOpcion.id = `${pos}-checkbox`;
                var td_pre = document.createElement('td');
                td_pre.appendChild(checkOpcion);

                trRow.appendChild(td_Nu);
                trRow.appendChild(td_I);
                trRow.appendChild(td_No);
                trRow.appendChild(td_pre);
                tbody.appendChild(trRow);

            });

            var contenedor = document.querySelector('#modal_funcionesBody');
            contenedor.appendChild(divTable);
            $('#tablaLista').DataTable({
                language: {
                    "sLengthMenu": "Mostrar _MENU_ registros",
                    "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                    "sZeroRecords": "No se encontraron resultados",
                    "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                    "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                    "sSearch": "Buscar:",
                    "oPaginate": {
                        "sFirst": "Primero",
                        "sLast": "Último",
                        "sNext": "Siguiente",
                        "sPrevious": "Anterior"
                    },
                }

            });

        })
        .catch(function (error) {
            console.error('Error:', error);
        });
}
let selectedOption = '';
function notas(id, nombre) {
    selectedOption = '';
    getData()
        .then(function (dataL) {
            var data = dataL;
            if (document.getElementById(id)) {
                console.log(id)
                $('#modal_funciones').modal('show');
            } else {
                var contenedor = document.querySelector('#modal_funcionesBody');
                contenedor.innerHTML = '';
                document.getElementById('modal_funcionesTitle').innerText = 'Añadir notas';
                var divRow = document.createElement('div');
                divRow.className = 'row';
                divRow.id = id;
                var divSelect = document.createElement('div');
                divSelect.className = 'form-group col-12 col-lg-3 col-md-6 col-sm-12';
                var label = document.createElement('label');
                label.className = '';
                label.setAttribute('for', 'parcial');
                label.innerText = 'Seleccione un examen'
                var select = document.createElement('select');
                select.className = 'form-select';
                select.id = 'selectExamen';
                var optionD = document.createElement('option');
                var optionE1 = document.createElement('option');
                var optionE2 = document.createElement('option');
                var optionEF = document.createElement('option');
                var optionEO = document.createElement('option');
                optionD.selected = true;
                optionD.disabled = true;
                optionD.hidden = true;
                optionD.innerText = 'Seleccione un examen';

                optionE1.value = 'Parcial1'
                optionE1.innerText = 'Evaluación 1';
                optionE2.value = 'Parcial2'
                optionE2.innerText = 'Evaluación 2';
                optionEF.value = 'ExamenF'
                optionEF.innerText = 'Evaluación Final';
                optionEO.value = 'Otras'
                optionEO.innerText = 'Otra evaluación';

                select.addEventListener('change', function (event) {
                    selectedOption = event.target.value;
                    habilitarInput(event.target.value)
                });

                select.appendChild(optionD);
                select.appendChild(optionE1);
                select.appendChild(optionE2);
                select.appendChild(optionEF);
                select.appendChild(optionEO);

                divSelect.appendChild(label);
                divSelect.appendChild(select);
                // var divInput = document.createElement('div');
                // divInput.className = 'form-group col-12 col-lg-4 col-md-6 col-sm-12';
                // divInput.style.display = 'none';
                // divInput.id = 'Parcial1';

                // var divInputII = document.createElement('div');
                // divInputII.className = 'form-group col-12 col-lg-4 col-md-6 col-sm-12';
                // divInputII.style.display = 'none';
                // divInputII.id = 'Parcial2';

                // var divInputIII = document.createElement('div');
                // divInputIII.className = 'form-group col-12 col-lg-4 col-md-6 col-sm-12';
                // divInputIII.style.display = 'none';
                // divInputIII.id = 'ExamenF';

                // var labelI = document.createElement('label');
                // labelI.className = '';
                // labelI.id = 'lbparcial1';
                // labelI.setAttribute('for', 'parcial1');
                // labelI.innerText = 'Añade el porcentaje del primer parcial';
                // var input = document.createElement('input');
                // input.className = 'form-control';
                // input.type = 'text';
                // input.id = 'parcial1';
                // input.placeholder = 'Porcentaje';

                // var labelII = document.createElement('label');
                // labelII.className = '';
                // labelI.id = 'lbparcial2';
                // labelII.setAttribute('for', 'parcial1');
                // labelII.innerText = 'Añade el porcentaje del segundo parcial';
                // var inputII = document.createElement('input');
                // inputII.className = 'form-control';
                // inputII.type = 'text';
                // inputII.id = 'parcial2';
                // inputII.placeholder = 'Porcentaje';

                // var labelIII = document.createElement('label');
                // labelIII.className = '';
                // labelI.id = 'lbparcial3';
                // labelIII.setAttribute('for', 'parcial1');
                // labelIII.innerText = 'Añade el porcentaje del examen final';
                // var inputIII = document.createElement('input');
                // inputIII.className = 'form-control';
                // inputIII.type = 'text';
                // inputIII.id = 'parcial3';
                // inputIII.placeholder = 'Porcentaje';

                // divInput.appendChild(labelI);
                // divInput.appendChild(input);
                // divInputII.appendChild(labelII);
                // divInputII.appendChild(inputII);
                // divInputIII.appendChild(labelIII);
                // divInputIII.appendChild(inputIII);
                var divRowAlert = document.createElement('div');
                divRowAlert.className = 'row ';
                var divAlert = document.createElement('div');
                divAlert.className = 'col-12 col-sm-12 col-md-12 col-lg-7 mx-auto';
                var divInfo = document.createElement('div');
                divInfo.className = 'alert alert-info';
                divInfo.role = 'alert';
                divInfo.style.display = 'block';
                divInfo.id = 'infoNota';
                var pInfo = document.createElement('p');
                pInfo.innerText = 'Valores permidos son: ';
                var ulInfo = document.createElement('ul');
                ulInfo.className = 'mb-0';
                var liInfoN = document.createElement('li');
                liInfoN.innerText = 'Entre 0 a 100';
                var liInfoNP = document.createElement('li');
                liInfoNP.innerText = 'NP (No se presento)';
                ulInfo.appendChild(liInfoN);
                ulInfo.appendChild(liInfoNP);
                divInfo.appendChild(pInfo);
                divInfo.appendChild(ulInfo);

                var divError = document.createElement('div');
                divError.className = 'alert alert-danger';
                divError.role = 'alert';
                divError.style.display = 'none';
                divError.id = 'errorNota';
                var ulError = document.createElement('ul');
                ulError.className = 'mb-0';
                var liError = document.createElement('li');
                liError.innerText = 'Valores invalidos, solo se permite valores entre 0 a 100 y NS, ND, GD';
                ulError.appendChild(liError);
                divError.appendChild(ulError);
                divAlert.appendChild(divInfo);
                divAlert.appendChild(divError);
                divRow.appendChild(divSelect);
                divRowAlert.appendChild(divAlert);
                // divRow.appendChild(divInput);
                // divRow.appendChild(divInputII);
                // divRow.appendChild(divInputIII);

                var divTable = document.createElement('div');
                divTable.className = 'table-responsive-lg mb-3';
                divTable.id = 'divTable';
                var table = document.createElement('table');
                table.className = 'table  dataTable';
                table.id = 'tablaLista';

                var thead = document.createElement('thead');
                var tr = document.createElement('tr');

                var thNu = document.createElement('th');
                thNu.scope = "col";
                thNu.appendChild(document.createTextNode('#'));

                var thC = document.createElement('th');
                thC.scope = "col";
                thC.appendChild(document.createTextNode('Identificación'));

                var thN = document.createElement('th');
                thN.scope = "col";
                thN.appendChild(document.createTextNode('Nombre'));

                var thP1 = document.createElement('th');
                thP1.scope = "col";
                thP1.appendChild(document.createTextNode('Evaluación 1'));

                var thP2 = document.createElement('th');
                thP2.scope = "col";
                thP2.appendChild(document.createTextNode('Evaluación 2'));

                var thP3 = document.createElement('th');
                thP3.scope = "col";
                thP3.appendChild(document.createTextNode('Evaluación Final'));

                var thP4 = document.createElement('th');
                thP4.scope = "col";
                thP4.appendChild(document.createTextNode('Otras evaluación'));

                tr.appendChild(thNu);
                tr.appendChild(thC);
                tr.appendChild(thN);
                tr.appendChild(thP1);
                tr.appendChild(thP2);
                tr.appendChild(thP3);
                tr.appendChild(thP4);

                thead.appendChild(tr);
                table.appendChild(thead);
                var tbody = document.createElement('tbody');
                tbody.id = 'listBody';
                table.appendChild(tbody);
                divTable.appendChild(table);

                data.forEach((estudiante, item) => {
                    var trRow = document.createElement('tr');
                    var td_Nu = document.createElement('td');
                    var pos = item + 1
                    td_Nu.appendChild(document.createTextNode(' ' + pos));

                    var td_I = document.createElement('td');
                    td_I.id = estudiante.carné;
                    td_I.appendChild(document.createTextNode(' ' + estudiante.carné));

                    var td_No = document.createElement('td');
                    td_No.appendChild(document.createTextNode(' ' + estudiante.nombre));

                    var td_P1 = document.createElement('td');
                    var inputP1 = document.createElement('input');
                    inputP1.className = 'form-control';
                    inputP1.id = 'par1' + estudiante.carné;
                    inputP1.readOnly = true;
                    inputP1.addEventListener('change', function () {
                        validarData('par1' + estudiante.carné, estudiante.carné, 'Parcial1', nombre);
                    })
                    if (inputP1.value.trim() === '') {
                        inputP1.value = obtenerValorNota(estudiante.carné, 'Parcial1', nombre);
                      }
                    td_P1.appendChild(inputP1);

                    var td_P2 = document.createElement('td');
                    var inputP2 = document.createElement('input');
                    inputP2.className = 'form-control';
                    inputP2.id = 'par2' + estudiante.carné;
                    inputP2.readOnly = true;
                    inputP2.addEventListener('change', function () {
                        validarData('par2' + estudiante.carné, estudiante.carné, 'Parcial2', nombre);
                    })
                    td_P2.appendChild(inputP2);

                    var td_P3 = document.createElement('td');
                    var inputP3 = document.createElement('input');
                    inputP3.className = 'form-control';
                    inputP3.id = 'par3' + estudiante.carné;
                    inputP3.readOnly = true;
                    inputP3.addEventListener('change', function () {
                        validarData('par3' + estudiante.carné, estudiante.carné, 'Parcial3', nombre);
                    })
                    td_P3.appendChild(inputP3);

                    var td_P4 = document.createElement('td');
                    var inputP4 = document.createElement('input');
                    inputP4.className = 'form-control';
                    inputP4.id = 'par4' + estudiante.carné;
                    inputP4.readOnly = true;
                    inputP4.addEventListener('change', function () {
                        validarData('par4' + estudiante.carné, estudiante.carné, 'Parcial4', nombre);
                    })
                    td_P4.appendChild(inputP4);

                    trRow.appendChild(td_Nu);
                    trRow.appendChild(td_I);
                    trRow.appendChild(td_No);
                    trRow.appendChild(td_P1);
                    trRow.appendChild(td_P2);
                    trRow.appendChild(td_P3);
                    trRow.appendChild(td_P4);
                    tbody.appendChild(trRow);
                });
                var divRowBotones = document.createElement('div');
                divRowBotones.className = 'row d-flex justify-content-end';
                var divColBotones = document.createElement('div');
                divColBotones.className = 'col-md-4';

                var divbutton0 = document.createElement('div');
                divbutton0.className = 'btn-group mr-2 col-md-3';
                divbutton0.role = 'group';
                divbutton0.style.display = 'none';
                divbutton0.id = 'parcialdiv1';
                var btnParcial1 = document.createElement('button');
                btnParcial1.className = 'btn btn-secondary';
                btnParcial1.type = 'button';
                btnParcial1.textContent = 'Subir evaluación 1';
                btnParcial1.disabled = true;
                divbutton0.appendChild(btnParcial1);

                var divbutton1 = document.createElement('div');
                divbutton1.className = 'btn-group mr-2 col-md-3';
                divbutton1.role = 'group';
                divbutton1.style.display = 'none';
                divbutton1.id = 'parcialdiv2';
                var btnParcial2 = document.createElement('button');
                btnParcial2.className = 'btn btn-secondary';
                btnParcial2.type = 'button';
                btnParcial2.textContent = 'Subir evaluación 2';
                btnParcial2.disabled = true;
                divbutton1.appendChild(btnParcial2);

                var divbutton2 = document.createElement('div');
                divbutton2.className = 'btn-group mr-2 col-md-3';
                divbutton2.role = 'group';
                divbutton2.style.display = 'none';
                divbutton2.id = 'parcialdiv3';
                var btnParcial3 = document.createElement('button');
                btnParcial3.className = 'btn btn-secondary';
                btnParcial3.type = 'button';
                btnParcial3.textContent = 'Subir evaluación final';
                btnParcial3.disabled = true;
                divbutton2.appendChild(btnParcial3);

                var divbutton3 = document.createElement('div');
                divbutton3.className = 'btn-group mr-2 col-md-3';
                divbutton3.role = 'group';
                divbutton3.style.display = 'none';
                divbutton3.id = 'parcialdiv4';
                var btnParcial4 = document.createElement('button');
                btnParcial4.className = 'btn btn-secondary';
                btnParcial4.type = 'button';
                btnParcial4.textContent = 'Subir otras evaluación';
                btnParcial4.disabled = true;
                divbutton3.appendChild(btnParcial4);

                divRowBotones.appendChild(divbutton0);
                divRowBotones.appendChild(divbutton1);
                divRowBotones.appendChild(divbutton2);
                divRowBotones.appendChild(divbutton3);

                contenedor.appendChild(divRow);
                contenedor.appendChild(divRowAlert);
                contenedor.appendChild(divTable);
                contenedor.appendChild(divRowBotones);
                $('#tablaLista').DataTable({
                    language: {
                        "sLengthMenu": "Mostrar _MENU_ registros",
                        "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                        "sZeroRecords": "No se encontraron resultados",
                        "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                        "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                        "sSearch": "Buscar:",
                        "oPaginate": {
                            "sFirst": "Primero",
                            "sLast": "Último",
                            "sNext": "Siguiente",
                            "sPrevious": "Anterior"
                        },
                    },
                    drawCallback: function () {
                        habilitarInput(selectedOption);
                    }

                });
                $('#modal_funciones').modal('show');
            }
        })
        .catch(function (error) {
            console.error('Error:', error);
        });

}

function habilitarInput(index) {
    const columns = $('#tablaLista tr').find('td:nth-child(4), td:nth-child(5), td:nth-child(6), td:nth-child(7)');
    columns.find('input').prop('readonly', true);

    // $('#Parcial1, #Parcial2, #ExamenF').hide();

    if (index === 'Parcial1') {
        const parcial1Column = $('#tablaLista tr').find('td:nth-child(4)');
        parcial1Column.find('input').prop('readonly', false);
        $('#Parcial1').show();
        $('#parcialdiv1').show();
        examenData = [];
        $('#parcialdiv2, #parcialdiv3, #parcialdiv4').hide();
    } else if (index === 'Parcial2') {
        const parcial2Column = $('#tablaLista tr').find('td:nth-child(5)');
        parcial2Column.find('input').prop('readonly', false);
        $('#Parcial2').show();
        $('#parcialdiv2').show();
        examenData = [];
        $('#parcialdiv1, #parcialdiv3, #parcialdiv4').hide();
    } else if (index === 'ExamenF') {
        const examenFColumn = $('#tablaLista tr').find('td:nth-child(6)');
        examenFColumn.find('input').prop('readonly', false);
        $('#ExamenF').show();
        $('#parcialdiv3').show();
        examenData = [];
        $('#parcialdiv1, #parcialdiv2, #parcialdiv4').hide();
    } else if (index === 'Otras') {
        const otrasColumn = $('#tablaLista tr').find('td:nth-child(7)');
        otrasColumn.find('input').prop('readonly', false);
        $('#ExamenF').show();
        $('#parcialdiv4').show();
        examenData = [];
        $('#parcialdiv1, #parcialdiv2, #parcialdiv3').hide();
    }
}

function calcular(idP, idIn) {
    var por = document.getElementById(idP);
    var nota = document.getElementById(idIn);

    var porcentaje = (por.value * nota.value) / 100;
    console.log(porcentaje);
}

let examenData = [];
function validarData(id ,idI, tipo, nombre) {
    var inputElement = document.getElementById(id);
    var inputValue = inputElement.value.trim();

    // Expresión regular para validar el texto de 0 a 100
    var textRegex = /^([0-9]{1,2}|100)$/;

    // Expresión regular para validar las opciones "NS", "DF" y "GT"
    var optionRegex = /^(NP|DF|GT)$/;

    // Validar el valor del campo de entrada
    if (textRegex.test(inputValue) || optionRegex.test(inputValue)) {
        // El valor es válido
        var identificacion = document.getElementById(idI); // Obtener la identificación desde la tabla
        if(tipo == 'Parcial1'){
            saveData(identificacion.innerText,inputValue,'Parcial1', nombre);
        }else if(tipo == 'Parcial2'){
            saveData(identificacion.innerText,inputValue,'Parcial2', nombre);
        }else if(tipo == 'Parcial3'){
            saveData(identificacion.innerText,inputValue,'Parcial3', nombre);
        }else{
            saveData(identificacion.innerText,inputValue,'Parcial4', nombre);
        }

    } else {
        // El valor no es válido, mostrar un mensaje de error
        document.getElementById('errorNota').style.display = 'block';
        document.getElementById('infoNota').style.display = 'none';
        setTimeout(function () {
            document.getElementById('errorNota').style.display = 'none';
            document.getElementById('infoNota').style.display = 'block';
        }, 5000);
        inputElement.setCustomValidity("Valor no válido: " + inputValue)
        inputElement.value = "";
        console.log("Valor no válido: " + inputValue);
    }
}

function saveData(id, nota, tipo, nombre){
    var nota = {
        'parcial': tipo,
        "identificacion": id,
        "nota": nota
    };
    examenData.push(nota);
    localStorage.setItem(nombre, JSON.stringify(examenData));
}

function obtenerValorNota(id, tipo, nombre){
    var notasJson = JSON.parse(localStorage.getItem(nombre));
    if (notasJson === null || notasJson === undefined) {
        return '';
    }
    var notaEncontrada = notasJson.find(function(nota) {
        return nota.identificacion === id && nota.parcial === tipo;
    });
    return notaEncontrada ? notaEncontrada.nota : '';
}