$(document).ready(function () {
    var idA = document.getElementById('accesibilidadId');
    idA.onclick = function () {
        mostrar();
    }
    var zoomIn = document.getElementById('zoomIn');
    zoomIn.onclick = function () {
        aumentarFuente();
    }

    var zoomOut = document.getElementById('zoomOut');
    zoomOut.onclick = function () {
        disminuirFuente();
    }

    var restablecer = document.getElementById('refres');
    restablecer.onclick = function () {
        restablecerFuente();
    }

    var daltonize = document.getElementById('daltonismType');
    daltonize.onchange = function () {
        changeColor();
    }

    var closeSocial = document.getElementById('closeSocial');
    closeSocial.onclick = function () {
        hideNavbar();
    }
    var openSocial = document.getElementById('openSocial');
    openSocial.onclick = function () {
        toggleNavbar();
    }

    const toggleButton = document.getElementById('accesibilidadId');
    const sidebar = document.querySelector('#contentA');
    const navbar = document.querySelector('#social-sidebar');

    toggleButton.addEventListener('click', () => {
        sidebar.classList.toggle('active');
        navbar.style.zIndex = sidebar.classList.contains('active') ? -1 : 10;
    });
    loadGoogleTranslateAPI();
    $('.google-translate-select').select2();
});

function mostrar() {
    var id = document.getElementById('contentA');
    if (id.style.display !== 'none') {
        id.style.display = 'none';
    } else {
        id.style.display = 'block';
    }
}

function aumentarFuente() {
    var contenido = document.getElementById('wrapper');
    var tamañoActual = window.getComputedStyle(contenido, null).getPropertyValue("font-size");
    var tamañoNuevo = parseInt(tamañoActual) + 2;
    contenido.style.fontSize = tamañoNuevo + "px";
}


function disminuirFuente() {
    var contenido = document.getElementById('wrapper');
    var tamañoActual = window.getComputedStyle(contenido, null).getPropertyValue("font-size");
    var tamañoNuevo = parseInt(tamañoActual) - 2;
    contenido.style.fontSize = tamañoNuevo + "px";
}

function restablecerFuente() {
    var contenido = document.getElementById('wrapper');
    contenido.style.fontSize = "";
}

function googleTranslateElementInit() {
    new google.translate.TranslateElement(
      {
        pageLanguage: 'es',
        autoDisplay: false,
        gaTrack: true,
      },
      'google_translate_element'
    );

    // Add 'select2' styles to the language dropdown
    const googleTranslateSelect = document.querySelector('.goog-te-combo');
    googleTranslateSelect.classList.add('google-translate-select');
    googleTranslateSelect.classList.add('form-select');
    $('#skiptranslate').text('Hola');
  }

  // Load the Google Translate API script
  function loadGoogleTranslateAPI() {
    const script = document.createElement('script');
    script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.body.appendChild(script);
  }

function changeColor() {
    var type = document.getElementById('daltonismType').value;
    var body = document.getElementById('bodyUia');
    if (type === 'normal') {
        console.log('Hola1');
        body.style.filter = 'none';
    } else if (type === 'protanopia') {
        console.log('Hola2');
        body.style.filter = 'url(#protanopia)';
    } else if (type === 'deuteranopia') {
        console.log('Hola3');
        body.style.filter = 'url(#deuteranopia)';
    } else if (type === 'tritanopia') {
        console.log('Hola4');
        body.style.filter = 'url(#tritanopia)';
    } else if (type === 'monochromacy') {
        console.log('Hola5');
        body.style.filter = 'url(#monochromacy)';
    } else if (type === 'enhance-r') {
        console.log('Hola6');
        body.style.filter = 'url(#enhance-r)';
    } else if (type === 'enhance-g') {
        console.log('Hola7');
        body.style.filter = 'url(#enhance-g)';
    }
}

function hideNavbar() {
    var navbars = document.querySelectorAll('#liSocial');
    var hideButton = document.getElementById('closeSocial');
    var toggleButton = document.getElementById('openSocial');
    var navbar = document.getElementById('social-sidebar');

    navbars.forEach(function (navbar) {
        navbar.style.display = 'none'; // Ocultar la barra de navegación
    });
    hideButton.style.display = 'none'; // Ocultar el botón de ocultar navbar
    toggleButton.style.display = 'block'; // Mostrar el botón de mostrar navbar
    
}

function toggleNavbar() {
    var navbar = document.querySelectorAll('#liSocial');
    var hideButton = document.getElementById('closeSocial');
    var toggleButton = document.getElementById('openSocial');
    navbar.forEach(function (navbar) {
        navbar.style.display = ''; // Ocultar la barra de navegación
    });
    hideButton.style.display = 'block'; // Mostrar el botón de ocultar navbar
    toggleButton.style.display = 'none'; // Ocultar el botón de mostrar navbar
}