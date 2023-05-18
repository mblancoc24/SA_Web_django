function time(){
    var time = document.getElementById("time");
    var url = "/obtener-time/";

    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = function () {
      if (request.status === 200) {
        time.value = JSON.parse(request.responseText);
      }
    };
    request.send();
}

