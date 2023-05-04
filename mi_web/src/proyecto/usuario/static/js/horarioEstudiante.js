$(document).ready(function () {
    addStyle();
    $('.curso').each(function () {
        $('.curso').hover(function () {
            var modal = document.querySelector('.horario');
            const text = $(this).text();
            var id = text+'curso';
            modal.id = id;
            $('#'+id).modal('show');
        });
    });
    
});
function addStyle() {
    $('.curso').each(function () {
        const text = $(this).text();
        const className = "curso-" + text.replace(/\W/g, '');
        let color = localStorage.getItem(className); // obtener el color almacenado
        if (!color) { // si no hay un color almacenado, generarlo
            const hue = Math.floor(Math.random() * 360);
            const saturation = 70; // fijar saturación al 70%
            const lightness = 50; // fijar luminosidad al 50%
            color = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
            localStorage.setItem(className, color); // almacenar el color generado
        }
        $(this).addClass(className);
        $(this).css('background-color', color);
        $(this).css('color', 'white');
        $(this).css('padding-top', '5px');
        $(this).css('padding-bottom', '5px');
        $(this).css('padding-left', '15px');
        $(this).css('padding-right', '15px');
        $(this).css('border-radius', '5px');
        $(this).css('margin-bottom', '10px');
        $(this).css('font-size', '16px');
    });
}

