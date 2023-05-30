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

    var traducir = document.getElementById('google_translate_element');
    traducir.onclick = function () {
        googleTranslateElementInit();
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
    var contenido = document.getElementsByTagName("body")[0];
    var footer = document.getElementsByTagName("footer")[0]; // Obtener el elemento del footer
    var tamañoActual = window.getComputedStyle(contenido, null).getPropertyValue("font-size");
    var tamañoActualF = window.getComputedStyle(footer, null).getPropertyValue("font-size");
    console.log(tamañoActualF + 'F');
    var tamañoNuevo = parseInt(tamañoActual) + 2;
    var tamañoNuevoF = parseInt(tamañoActualF) + 2;
    contenido.style.fontSize = tamañoNuevo + "px";
    footer.style.fontSize = tamañoNuevoF + "px"; // Aumentar el tamaño de fuente del footer
}


function disminuirFuente() {
    var contenido = document.getElementsByTagName("body")[0];
    var footer = document.getElementsByTagName("footer")[0]; // Obtener el elemento del footer
    var tamañoActual = window.getComputedStyle(contenido, null).getPropertyValue("font-size");
    var tamañoNuevo = parseInt(tamañoActual) - 2;
    contenido.style.fontSize = tamañoNuevo + "px";
    footer.style.fontSize = tamañoNuevo + "px"; // Aumentar el tamaño de fuente del footer
}

function restablecerFuente() {
    var contenido = document.getElementsByTagName("body")[0];
    contenido.style.fontSize = "";
}

function googleTranslateElementInit() {
    var allLanguages = [
        'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh-CN',
        'zh-TW', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka',
        'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it',
        'ja', 'jw', 'kn', 'kk', 'km', 'rw', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk',
        'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt',
        'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su',
        'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy',
        'xh', 'yi', 'yo', 'zu'
    ];

    var allLanguagesString = allLanguages.join(',');

    new google.translate.TranslateElement({
        pageLanguage: 'es',
        includedLanguages: allLanguagesString,
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE
    }, 'google_translate_element');
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