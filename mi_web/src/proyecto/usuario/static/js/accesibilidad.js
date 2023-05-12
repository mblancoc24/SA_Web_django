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
    var tamañoActual = window.getComputedStyle(contenido, null).getPropertyValue("font-size");
    var tamañoNuevo = parseInt(tamañoActual) + 2;
    contenido.style.fontSize = tamañoNuevo + "px";
}

function disminuirFuente() {
    var contenido = document.getElementsByTagName("body")[0];
    var tamañoActual = window.getComputedStyle(contenido, null).getPropertyValue("font-size");
    var tamañoNuevo = parseInt(tamañoActual) - 2;
    contenido.style.fontSize = tamañoNuevo + "px";
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